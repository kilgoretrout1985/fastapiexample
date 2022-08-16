from fastapi import Request


async def add_custom_header_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-My-Custom-Header-For-Test"] = "my header data"
    return response
