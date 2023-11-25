from dao.base_dao import BaseDao
from dao.po.tb_task_po import TbTaskPo
sql_tb_task = "create table if not exists tb_task(`id` integer primary key autoincrement,`config_id` integer not null, `sync_src` varchar(255),`sync_dest` varchar(255),`type`int(4) NOT NULL,`schedule` text,`state` int(4) default 0,`deleted` int(4) default 0,`create_time` timestamp  default(datetime(CURRENT_TIMESTAMP,'localtime')),`update_time` timestamp default(datetime(CURRENT_TIMESTAMP,'localtime')) ,CONSTRAINT  `ssc` UNIQUE (`config_id`,`sync_src`,`sync_dest`) )"



class TbTaskDao(BaseDao):
    def create_tb(self):
        return sql_tb_task

    def add(self, po: TbTaskPo):
        sql = "insert into tb_task(`config_id`,`type`,`sync_src`,`sync_dest`,`schedule`,`state`) values (?,?,?,?,?,?)"
        self.exe_sql(sql, (po.config_id, po.type, po.sync_src, po.sync_dest, po.schedule,po.state))

    def delete(self, id):
        sql = "delete from tb_task where id=?"
        self.exe_sql(sql, (id))

    def update_path(self, sync_src, sync_dest, id):
        sql = "update tb_task set `sync_src`=? , sync_dest=?  where id=?"
        self.exe_sql(sql, (sync_src, sync_dest, id))

    def update_src_path(self, sync_src,  id):
        sql = "update `tb_task` set `sync_src`= ? where id = ? "
        self.exe_sql(sql, (sync_src, id))

    def update_schedule(self, schedule, id):
        sql = "update tb_task set `schedule`=? where id=?"
        self.exe_sql(sql, (schedule, id))

    def update_state(self, state, id):
        sql = "update tb_task set `state`=? where id=?"
        self.exe_sql(sql, (state, id))

    def list(self):
        sql = "select * from tb_task"
        return self.exe_sql(sql)
    def query(self,config_id:int):
        sql = "select * from tb_task where config_id=?"
        return self.exe_sql(sql, [config_id])