from fastapi import APIRouter, Request, Path, Query, Body

from dao.po.tb_config_po import TbConfigPo
from dao.init_dao import tbConfigDao, tbTaskDao
from api.base_api import ok, fail

from sdk.Config import WebDavConfig
from sdk import WebDav

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
    return ok(tbConfigDao.list())


# 删除指定配置
@router.delete("/api/v1/config/{id}")
async def delete_config(id: int = Path(...)):
    list = tbTaskDao.query(config_id=id)
    if len(list) == 0:
        tbConfigDao.delete(id)
        return ok()
    else:
        return fail("该配置下有任务，不能删除配置，请先取消任务")


# 更新配置
@router.put("/api/v1/config/{id}")
async def config_update(id: int = Path(...),
                        username: str = Body(...), password: str = Body(...), type: int = Body(0)):
    if password != None:
        tbConfigDao.update_password(password, id)
    if username != None:
        tbConfigDao.update_username(username, id)
    if type != None and type > 0:
        tbConfigDao.update_type(type, id)
    return ok("")


# 测试配置接口
@router.post("/api/v1/config/test")
async def config_test(host: str = Body(...),
                      username: str = Body(...), password: str = Body(...)):
    options = {
        'webdav_hostname': host,
        'webdav_login': username,
        'webdav_password': password,
        "disable_check": True,
    }
    config = WebDavConfig(options,None)
    if WebDav.test(config):
        return ok()
    else:
        return fail("配置不可用")
