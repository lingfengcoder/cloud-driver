import json
import sys
from sdk.log import logger
import sqlite3
from dao import init_dao
from dao.base_dao import db
from dao.init_dao import tbConfigDao
from dao.init_dao import tbTaskDao
from dao.po.tb_task_po import TbTaskPo
from dao.po.tb_config_po import TbConfigPo


class test:

    def drop_table(self):
        conn = sqlite3.connect(db)
        conn.execute("drop table if  exists tb_config")
        conn.execute("drop table if  exists tb_task")
        conn.commit()
        conn.close()

    def init_table(self):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        # cur.execute(sql_tb_config)
        # cur.execute(sql_tb_task)
        conn.commit()
        conn.close()

    def init_data(self):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql1 = "insert into tb_config(`type`,`host`,`username`,`password`) values (1,'host','uname','pwd')"
        sql2 = "insert into tb_task(`config_id`,`sync_src`,`sync_dest`,`type`,`schedule`,`state`) values (1,'/alist/movie','/mnt/user/movie2/',1,'schedule_task',0)"
        try:
            res = cur.execute(sql1)
            logger.info(res)
            res = cur.execute(sql2)
            logger.info(res)
        except Exception as err:
            logger.error("sql执行错误 err=%s msg:%s" % (err.__class__, err))
        conn.commit()

        cur.execute("select * from tb_config")
        list1 = cur.fetchall()
        logger.info(list1)

        cur.execute("select * from tb_task")
        list2 = cur.fetchall()
        logger.info(list2)
        conn.close()


if __name__ == '__main__':
    init_dao.init()
    # tbConfigDao.delete_by_ids((9,10,11))
    list = tbConfigDao.list()

    j_list = json.dumps(list)
    logger.info(j_list)
    for item in list:
        tbConfigDao.delete(item['id'])
    param = TbConfigPo(1, 'host-2', 'uname-2', 'pwd-2')
    tbConfigDao.add(param)

    list = tbTaskDao.list()
    logger.info(list)
    param=TbTaskPo(1, 'sync_src-1', 'sync_dest-1', 1,"schedule-1",0)
    tbTaskDao.add(param)
