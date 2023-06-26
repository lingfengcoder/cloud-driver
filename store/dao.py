# 文件存储系统
import sys
import sqlite3


class StoreService:
    path = ""

    def init(self):
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        # sql="drop table base_info"
        # cur.execute(sql)

        # id type
        # sql = "create table base_info(`id` integer PRIMARY KEY AUTOINCREMENT,`type` int(4) NOT NULL, `host` varchar(255),`username` varchar(127),`password` varchar(64),`deleted` int(4) default 0,`create_time` timestamp,`update_time` timestamp)"
        #
        #
        # cur.execute(sql)

        # sql1="insert into base_info(`type`,`host`,`username`,`password`,`deleted`,`create_time`,`update_time`) values (1,'host','uname','pwd',0,'2023-06-24 14:47:00',NULL)"
        #
        # cur.execute(sql1)
        # conn.commit()

        sql2="select * from base_info"

        cur.execute(sql2)

        list= cur.fetchall()
        conn.close()

if __name__ == '__main__':
   ss= StoreService()
   ss.init()