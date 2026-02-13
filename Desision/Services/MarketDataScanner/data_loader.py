import pandas as pd
from Desision.database.repository import OHLCRepository
from Desision.Services.MarketDataScanner.validate import KlineValidator, KlineNormalizer
from Desision.Services.MarketDataScanner.persist import klines_to_rows
from config import CATEGORY

repo = OHLCRepository()

def load_symbol_data(symbol: str, interval: str) -> pd.DataFrame:

    existing_df = repo.fetch_ohlc(symbol, interval, limit=1000)

    # REST запрос
    from Desision.Services.MarketDataScanner.top_volume_usdt import TopVolumeUSDTService
    service = TopVolumeUSDTService(testnet=False)

    response = service.session.get_kline(
        category=CATEGORY,
        symbol=symbol,
        interval=interval,
        limit=1000,
    )

    raw = response.get("result", {}).get("list")
    if not isinstance(raw, list):
        return existing_df

    klines = KlineNormalizer.from_rest(raw, symbol=symbol, interval=interval)

    if not KlineValidator.validate(klines):
        return existing_df

    rows = klines_to_rows(klines)

    if rows:
        repo.insert_ohlc(rows)

    new_df = pd.DataFrame(rows)

    if not new_df.empty:
        df = pd.concat([existing_df.reset_index(), new_df])
    else:
        df = existing_df.reset_index()

    df.reset_index(drop=True, inplace=True)
    return df
