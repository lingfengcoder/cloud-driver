import logging

from dao.base_dao import BaseDao
from dao.po.tb_config_po import TbConfigPo
sql_tb_config = "create table if not exists tb_config(`id` integer PRIMARY KEY AUTOINCREMENT,`type` int(4) NOT NULL, `host` varchar(255) UNIQUE,`username` varchar(127),`password` varchar(64),`deleted` int(4) default 0,`create_time` timestamp  default(datetime(CURRENT_TIMESTAMP,'localtime')),`update_time` TIMESTAMP default(datetime(CURRENT_TIMESTAMP,'localtime')) )"



class TbConfigDao(BaseDao):
    def create_tb(self):
        return sql_tb_config

    def add(self, po:TbConfigPo):
        sql = "insert into tb_config(`type`,`host`,`username`,`password`) values (?,?,?,?)"
        self.exe_sql(sql, (po.type, po.host, po.username, po.password))

    def delete(self, id):
        sql = "delete from tb_config where id=?"
        self.exe_sql(sql, [id])

    def delete_by_ids(self, ids:()):
        ids_str=",".join(map(str, ids))
        sql = "delete from tb_config where id in ( %s ) "%(ids_str)
        self.exe_sql(sql)
    def update_username(self, username, id):
        sql = "update tb_config set `username`=? where id=?"
        self.exe_sql(sql, (username, id))

    def update_password(self, password, id):
        sql = "update tb_config set `password`=? where id=?"
        self.exe_sql(sql, (password, id))

    def list(self):
        sql = "select * from tb_config"
        list=self.exe_sql(sql, ())
        for item in list:
            item['password']="***"
        return list
