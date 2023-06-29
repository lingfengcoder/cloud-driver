from dao.tb_config_dao import TbConfigDao
from dao.tb_task_dao import TbTaskDao
from sdk.log import logger

tbConfigDao=TbConfigDao()
tbTaskDao=TbTaskDao()

def init():
    global tbConfigDao
    global tbTaskDao
    tbConfigDao = TbConfigDao()
    tbTaskDao = TbTaskDao()
