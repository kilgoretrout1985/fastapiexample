from sys import modules

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_DSN = "postgresql+asyncpg://fastapiexamplepguser:pass@localhost/fastapiexample"
do_echo_flag = True  # set True to see generated SQL queries in the console
# different postgres db for test runs
if 'pytest' in modules:
    DB_DSN = "postgresql+asyncpg://fastapiexamplepguser:pass@localhost/fastapiexample_test"
    do_echo_flag = False

engine = create_async_engine(DB_DSN, echo=do_echo_flag)
Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    # in async settings we don't want SQLAlchemy to issue new SQL queries
    # to the database when accessing already commited objects.
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with async_session() as db:
        yield db


async def init_models(delete_all=False):
    async with engine.begin() as conn:
        if delete_all:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
