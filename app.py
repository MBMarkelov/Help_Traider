def main():
    # 1. Проверяем БД
    from Desision.database.connection import get_connection
    conn = get_connection()
    conn.close()
    # 3. Здесь же могут стартовать:
    # start_pattern_engine()
    # start_api()


if __name__ == "__main__":
    main()
