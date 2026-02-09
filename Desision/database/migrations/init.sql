CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS ohlc (
    symbol      TEXT NOT NULL,
    interval    TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL,
    open        NUMERIC NOT NULL,
    high        NUMERIC NOT NULL,
    low         NUMERIC NOT NULL,
    close       NUMERIC NOT NULL,
    volume      NUMERIC NOT NULL,
    turnover    NUMERIC,
    PRIMARY KEY (symbol, interval, ts)
);

SELECT create_hypertable(
    'ohlc',
    'ts',
    if_not_exists => TRUE
);
