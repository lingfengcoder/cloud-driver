from fastapi import APIRouter, Request, Path, Query, Body

from dao.po.tb_task_po import TbTaskPo
from dao.init_dao import tbConfigDao, tbTaskDao
from api.base_api import ok, fail

router = APIRouter()


# 添加新的
@router.post("/api/v1/task/new")
async def add(po: TbTaskPo):
    config = tbConfigDao.query_by_id(po.config_id)
    if config == None:
        return fail("所选配置不存在")
    tbTaskDao.add(po)
    return ok()


# 获取所有的(未分页)
@router.get("/api/v1/task/all")
async def all():
    return tbTaskDao.list()


# 删除指定
@router.delete("/api/v1/task/{id}")
async def delete(id: int):
    tbTaskDao.delete(id)
    return ok()


# 更新
@router.put("/api/v1/task/{id}")
async def update(id: int = Path(...),
                 sync_src: str = Body(""), sync_dest: str = Body(""), schedule: str = Body("")):
    if sync_src != None and len(sync_src) > 0:
        tbTaskDao.update_path(sync_src=sync_src, sync_dest=sync_dest, id=id)
    if schedule != None:
        tbTaskDao.update_schedule(schedule, id)
    return ok()

@router.put("/api/v1/task/state/{id}")
async def state(id: int = Path(...),
                state: int = Query(...)):
    tbTaskDao.update_state(state, id)
    return ok()
