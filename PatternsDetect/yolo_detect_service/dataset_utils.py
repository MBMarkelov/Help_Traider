import pandas as pd
import mplfinance as mpf
import os


def crop_window(df, idx, window=60):
    left = max(0, idx - window)
    right = min(len(df), idx + window)
    return df.iloc[left:right].copy()


def save_pattern_png(
    df: pd.DataFrame,
    pattern_indices: list[int],
    symbol: str,
    pattern_type: str,
    output_dir: str,
    context_before: int = 60,
    context_after: int = 20,
):
    """
    Рендерит PNG только вокруг найденного паттерна.
    """

    os.makedirs(output_dir, exist_ok=True)

    df = df.copy()
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)

    for idx in pattern_indices:

        start = max(0, idx - context_before)
        end = min(len(df), idx + context_after)

        window = df.iloc[start:end]

        # mplfinance требует стандартные названия
        window = window.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        })

        save_path = os.path.join(
            output_dir,
            f"{symbol}_{pattern_type}_{idx}.png"
        )

        mpf.plot(
            window,
            type='candle',
            style='charles',
            figsize=(6, 4),        # важно для YOLO
            tight_layout=True,
            scale_padding=0.15,   # уменьшает “воздух”
            yscale='log',
            volume=False,
            axisoff=True,
            savefig=dict(
                fname=save_path,
                dpi=110,
                bbox_inches="tight",
                pad_inches=0.05
            )
        )