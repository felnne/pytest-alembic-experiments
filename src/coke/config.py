from os import environ

db_dsn = environ.get('APP_DB_DSN')

if __name__ == "__main__":
    print(db_dsn)
