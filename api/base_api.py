from fastapi import APIRouter, Request, Path, Query, Body
from task import TaskCenter
from dao.init_dao import tbTaskDao
from starlette.responses import JSONResponse

router = APIRouter()


def ok(data=None):
    return JSONResponse({"code": 200, "data": data, "msg": "success"})
def fail(msg):
    return JSONResponse({"code": 400, "msg": msg})

@router.get("/api/v1/hw")
def read_root():
    return {"Hello": "World"}

@router.get("/api/v1/webdav/new")
def task_list():
    return TaskCenter.new_task()


@router.get("/api/v1/webdav/alltask")
def task_list():
    return tbTaskDao.list()


@router.get("/api/v1/webdav/{task_id}/stop")
def stop(task_id: str):
    return TaskCenter.stop_task(task_id)


@router.get("/api/v1/webdav/{task_id}/restart")
def restart_task(task_id: str):
    return TaskCenter.restart_task(task_id)


@router.get("/api/v1/webdav/{task_id}/get_task_process")
def get_task_process(task_id: str):
    return TaskCenter.get_task_process(task_id)
