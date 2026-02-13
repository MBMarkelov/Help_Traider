# database/connection.py
import psycopg2
from .config import get_db_config


def get_connection():
    cfg = get_db_config()

    missing = [k for k, v in cfg.items() if v is None]
    if missing:
        raise RuntimeError(f"Missing DB config keys: {missing}")

    return psycopg2.connect(**cfg)

