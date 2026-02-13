from psycopg2.extras import execute_values
import pandas as pd
from .connection import get_connection



class OHLCRepository:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit = True

    def insert_ohlc(self, rows: list[dict]):
        sql = """
        INSERT INTO ohlc (
            symbol, interval, ts,
            open, high, low, close,
            volume, turnover
        ) VALUES %s
        ON CONFLICT DO NOTHING
        """

        values = [
            (
                r["symbol"],
                r["interval"],
                r["ts"],
                r["open"],
                r["high"],
                r["low"],
                r["close"],
                r["volume"],
                r.get("turnover")
            )
            for r in rows
        ]

        with self.conn.cursor() as cur:
            execute_values(cur, sql, values)

    def fetch_ohlc(self, symbol: str, interval: str, limit: int = 1000) -> pd.DataFrame:
        query = f"""
        SELECT ts, open, high, low, close, volume
        FROM ohlc
        WHERE symbol = %s AND interval = %s
        ORDER BY ts ASC
        LIMIT %s
        """
        # Используем безопасные параметры вместо f-string
        df = pd.read_sql(query, con=self.conn, params=(symbol, interval, limit))

        if df.empty:
            return df

        # Приводим ts к datetime
        df['ts'] = pd.to_datetime(df['ts'])
        df.set_index('ts', inplace=True)
        return df

