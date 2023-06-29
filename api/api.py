from fastapi import APIRouter
from task import TaskCenter
from dao.init_dao import tbTaskDao
from dao.po.tb_config_po import TbConfigPo
from dao.po.tb_task_po import TbTaskPo
from dao.init_dao import tbConfigDao
from api.result import ok,fail

router = APIRouter()


@router.get("/api/v1/hw")
def read_root():
    return {"Hello": "World"}


@router.get("/api/v1/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# tb_config
@router.put("/api/v1/config/new")
async def add_config(po:TbConfigPo):
    tbConfigDao.add(po)
    return ok()


@router.get("/api/v1/config/all")
async def task_list():
    return tbConfigDao.list()


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
