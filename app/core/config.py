from pydantic import PostgresDsn
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class Settings:
    POSTGRES_USER = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
    POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str)
    POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
    POSTGRES_DB = config("POSTGRES_DB", cast=str)

    SQLALCHEMY_DATABASE_URI: str = PostgresDsn.build(
        scheme="postgresql",
        user=POSTGRES_USER,
        password=str(POSTGRES_PASSWORD),
        host=POSTGRES_SERVER,
        port=POSTGRES_PORT,
        path=f"/{POSTGRES_DB or ''}",
    )
    POOL_SIZE = config("POOL_SIZE", cast=int, default=5)
    MAX_OVERFLOW = config("MAX_OVERFLOW", cast=int, default=-1)
    POOL_PRE_PING = config("POOL_PRE_PING", cast=bool, default=True)
    ECHO = config("ECHO", cast=bool, default=False)
    POOL_RECYCLE_IN_SECONDS = config("POOL_RECYCLE_IN_SECONDS", cast=int, default=3600)
    ECHO_POOL = config("ECHO_POOL", cast=bool, default=False)
    POOL_RESET_ON_RETURN = config("POOL_RESET_ON_RETURN", cast=str, default="rollback")
    POOL_TIMEOUT_IN_SECONDS = config("POOL_TIMEOUT_IN_SECONDS", cast=int, default=30)
    POOL = config("POOL", cast=str, default="~sqlalchemy.pool.QueuePool")
    REDIS_URL = config("REDIS_URL", cast=str)

    MONGO_USER = config("MONGO_USER", cast=str)
    MONGO_PASSWORD = config("MONGO_PASSWORD", cast=Secret)
    MONGO_SERVER = config("MONGO_SERVER", cast=str)
    MONGO_PORT = config("MONGO_PORT", cast=int, default=27017)
    MONGO_DB = config("MONGO_DB", cast=str)


settings = Settings()
