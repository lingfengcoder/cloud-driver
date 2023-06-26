import uvicorn
from fastapi import FastAPI
from api import api
from task import TaskCenter
from sdk.log import logger
import socket

app = FastAPI()
app.include_router(api.router)


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
    uvicorn.run(app, host=ip, port=8000)
