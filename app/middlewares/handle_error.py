from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
# import time

class ErrorHandler(BaseHTTPMiddleware):
  def __init__(self, app: FastAPI):
    super().__init__(app)
  async def dispatch(self, request: Request, call_next: Callable) -> Response | JSONResponse:
    try:
      return await call_next(request)
    except Exception as e:
      print(f"MAIN Error Handler Exception: {str(e)}")
      return JSONResponse(status_code=500, content={'error': str(e)})

# @router_middleware.middleware("http")
# async def error_handler(request: Request, next_call: Callable):
#   try:
#     start_time = time.time()
#     response = await next_call(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
#   except Exception as e:
#     print(f"MAIN Error Handler Exception: {str(e)}")
#     return JSONResponse(status_code=500, content={'error': str(e)})
