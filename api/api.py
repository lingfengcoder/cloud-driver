
from fastapi import APIRouter
from task import TaskCenter
router = APIRouter()


@router.get("/api/v1/hw")
def read_root():
    return {"Hello": "World"}

@router.get("/api/v1/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@router.get("/api/v1/webdav/new")
def task_list():
    return TaskCenter.new_task()
@router.get("/api/v1/webdav/alltask")
def task_list():
    return TaskCenter.task_list()

@router.get("/api/v1/webdav/{task_id}/stop")
def stop(task_id: str):
    return TaskCenter.stop_task(task_id)


@router.get("/api/v1/webdav/{task_id}/restart")
def restart_task(task_id: str):
    return TaskCenter.restart_task(task_id)


@router.get("/api/v1/webdav/{task_id}/get_task_process")
def get_task_process(task_id: str):
    return TaskCenter.get_task_process(task_id)