from psycopg2.extras import execute_values
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
