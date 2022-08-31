import asyncio
from typing import Dict

from fastapi import FastAPI
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from typer import Typer

from fastapiexample.middleware import add_custom_header_middleware
from fastapiexample.database import init_models
from fastapiexample.routers import users, items
from fastapiexample.config import settings


app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(users.router)
app.include_router(items.router)

app.middleware("http")(add_custom_header_middleware)
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware)

cli = Typer()


@cli.command()
def init_db(drop_all: bool = False):
    asyncio.run(init_models(drop_all))
    print("DB tables created.")


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    cli()
