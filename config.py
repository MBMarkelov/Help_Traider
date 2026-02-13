# config.py
DB_HOST="timescaledb"
DB_PORT=5432
DB_NAME="market_data"
DB_USER="trader"
DB_PASSWORD="trader"


# WebSocket конфигурация
DEFAULT_SYMBOLS="BTCUSDT","ETHUSDT"
DEFAULT_INTERVALS=5,15,60,240,"D"
TOP_N = 10
STABLES = ("USDT", "USDC", "USDE", "DAI")
CATEGORY = "spot"

BYBIT_REST_TESTNET = False
BYBIT_WS_URL = "wss://stream.bybit.com/v5/public/spot"

TOP_REFRESH_INTERVAL = 60  # сек

# Логирование
LOG_LEVEL="INFO"
LOG_FILE="/app/logs/ohlc_collector.log"

# Приложение
BATCH_SIZE=1000
INSERT_INTERVAL=1.0
MAX_RETRIES=5
RETRY_DELAY=5.0

INTERVAL = "60"
OUTPUT_DIR = "./cache"
TRIANGLE_TYPES = ["ascending", "descending", "symmetrical"]
WINDOW = 100
MIN_GAP = 15
LOOKBACK = 25
