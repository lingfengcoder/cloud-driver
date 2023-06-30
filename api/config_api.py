from fastapi import APIRouter, Request, Path, Query, Body

from dao.po.tb_config_po import TbConfigPo
from dao.init_dao import tbConfigDao, tbTaskDao
from api.base_api import ok, fail

router = APIRouter()

# tb_config
# 添加新的配置
@router.post("/api/v1/config/new")
async def add_config(po: TbConfigPo):
    tbConfigDao.add(po)
    return ok("")


# 获取所有的配置(未分页)
@router.get("/api/v1/config/all")
async def config_list():
    return tbConfigDao.list()


# 删除指定配置
@router.delete("/api/v1/config/{id}")
async def delete_config(id: int=Path(...)):
    list = tbTaskDao.query(config_id=id)
    if len(list) == 0:
        tbConfigDao.delete(id)
        return ok()
    else:
        return fail("该配置下有任务，不能删除配置，请先取消任务")


# 更新配置
@router.put("/api/v1/config/{id}")
async def config_update(id: int = Path(...),
                        uname: str = Body(...), pwd: str = Body(...), type: int = Body(0)):
    if pwd != None:
        tbConfigDao.update_password(pwd, id)
    if uname != None:
        tbConfigDao.update_username(uname, id)
    if type != None and type > 0:
        tbConfigDao.update_type(type, id)
    return ok("")
