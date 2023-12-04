from datetime import datetime

from fastapi import APIRouter, Request, Path, Query, Body

from api.dto.tb_task_dto import TbTaskDto
from dao.po.tb_task_po import TbTaskPo
from dao.init_dao import tbConfigDao, tbTaskDao
from api.base_api import ok, fail
import json
router = APIRouter()


# 添加新的
@router.post("/api/v1/task/new")
async def add(dto: TbTaskDto):
    config = tbConfigDao.query_by_id(dto.config_id)
    if config == None:
        return fail("所选配置不存在")
    po = TbTaskPo(id=0, config_id=dto.config_id, type=dto.type, sync_src=dto.sync_src, sync_dest=dto.sync_dest,
                  schedule=json.dumps(dto.schedule), state=dto.state,  update_time=datetime.now())
    tbTaskDao.add(po)
    return ok()


# 获取所有的(未分页)
@router.get("/api/v1/task/all")
async def all():
    data = tbTaskDao.list()
    return ok(data)


# 删除指定
@router.delete("/api/v1/task/{id}")
async def delete(id: int):
    tbTaskDao.delete(id)
    return ok()


# 更新 任务
@router.put("/api/v1/task/{id}")
async def update(id: int = Path(...),
                 sync_src: str = Body(""), sync_dest: str = Body(""), schedule: str = Body("")):
    if sync_src != None and len(sync_src) > 0:
        tbTaskDao.update_path(sync_src=sync_src, sync_dest=sync_dest, id=id)
    if schedule != None:
        tbTaskDao.update_schedule(schedule, id)
    return ok()


# 更新 state
@router.put("/api/v1/task/state/{id}")
async def state(id: int = Path(...),
                state: int = Query(...)):
    tbTaskDao.update_state(state, id)
    return ok()


# 更新 schedule
@router.put("/api/v1/task/schedule/{id}")
async def schedule(id: int = Path(...),
                   schedule: str = Query(...)):
    tbTaskDao.update_schedule(schedule, id)
    return ok()


# 更新 sync_src sync_dest
@router.put("/api/v1/task/path/{id}")
async def path(id: int = Path(...),
               sync_src: str = Query(...), sync_dest: str = Query(...)):
    tbTaskDao.update_path(sync_src=sync_src, sync_dest=sync_dest, id=id)
    return ok()


# 更新 config_id
@router.put("/api/v1/task/config/{id}")
async def config(id: int = Path(...),
                 config_id: int = Query(...)):
    tbTaskDao.update_config(config_id, id)
    return ok()
