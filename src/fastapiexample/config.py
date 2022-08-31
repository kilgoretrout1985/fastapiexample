from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "FastAPI example app"
    app_description: str = "Just a fastapi-framework example playground."

    # postgresql+asyncpg://user:[password]@host_or_ip[:port]/database_name
    db_dsn: str = "postgresql+asyncpg://fastapiexamplepguser:pass@localhost/fastapiexample"
    db_test_dsn: str = db_dsn + "_test"  # separate db to run tests is `fastapiexample_test` (same user, pass as ^^^)
    db_echo_flag: bool = True  # set True to see generated SQL queries in the console


settings = Settings()
