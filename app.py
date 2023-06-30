import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlite3 import DatabaseError
from sqlite3 import IntegrityError
from requests import Request
from starlette.responses import JSONResponse

from api.base_api import fail
from api import base_api
from api import config_api
from api import task_api
from task import TaskCenter
from sdk.log import logger
import socket

app = FastAPI()
app.include_router(base_api.router)
app.include_router(config_api.router)
app.include_router(task_api.router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"参数不对{request.method} {request.url}")
    return fail(exc.errors())


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    logger.error(f"sql 错误   {request.url} {exc.args}")
    return fail(msg=exc.args)

@app.exception_handler(IntegrityError)
async def database_exception_handler(request: Request, exc: IntegrityError):
    logger.error(f"数据重复 错误   {request.url} {exc.args}")
    return fail(msg=f"数据重复 错误  {exc.args}")

@app.on_event("shutdown")
async def shutdown_event():
    print("关闭应用程序")
    TaskCenter.shutdown("shutdown_event")


def get_ip_address():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


if __name__ == "__main__":
    ip = get_ip_address()
    logger.info("ip=%s" % ip)
    uvicorn.run(app,  port=8000)
