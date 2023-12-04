# 定时扫描任务表，将新的任务加入将关闭的任务剔除
from sdk.log import logger
import time
import threading
from task import TaskCenter
from dao.po.tb_task_po import TbTaskPo
from dao.po.tb_config_po import TbConfigPo
from dao.init_dao import tbConfigDao, tbTaskDao
from sdk.WebDav import TASK_STATE


class JobSchedule:

    def __init__(self):
        self.SHUT_DOWN = False
        self.THREAD = None
        # self.job = job

    def run(self):
        self.time_work(None)

    def daemon_work(self, callback):
        while (1):
            if self.SHUT_DOWN: break
            logger.info("定时任务扫描")
            try:
                taskList = tbTaskDao.list()

                # 循环taskList找出禁用和启用的
                for t in taskList:
                    task = TbTaskPo(**t)
                    # 如果是禁用的则停止
                    if task.state == 0:
                        TaskCenter.stop_task(task.id)
                        # 停止
                        pass
                    # 如果是启用的则启动
                    else:
                        run_task_config = TaskCenter.get_taskConfig(task.id)
                        if run_task_config == None and task.state == TASK_STATE.RUN:
                            logger.info("任务不存在,创建新的任务 id=%s" % task.id)
                            # 创建新的任务
                            c = tbConfigDao.query_by_id(task.config_id)
                            config = TbConfigPo(**c)
                            TaskCenter.new_task(task, config, task.update_time)
                        else:
                            if run_task_config != None:
                                if task.update_time != run_task_config.lastUpdateTime:
                                    # 更新定时任务
                                    logger.info("任务存在,更新定时任务 id=%s" % task.id)
                                    TaskCenter.update_schedule(task.id, task.schedule, task.update_time)
                                if TaskCenter.is_task_error(task.id):
                                    logger.info("任务存在,但是出现错误,重新启动 id=%s" % task.id)
                                    TaskCenter.stop_task(task.id)
                                    TaskCenter.delete_task(task.id)
                                    tbTaskDao.update_state(TASK_STATE.ERROR, task.id)
                                if TaskCenter.is_task_pause(task.id):
                                    logger.info("任务存在,但是出现暂停,重新启动 id=%s" % task.id)
                                    TaskCenter.restart_task(task.id)
                        # 启动
                        pass
            except Exception as e:
                logger.error("mainloop-error:%s" % e)
                # count += 10
            time.sleep(5)
            # time.sleep(10 * 60)

    def time_work(self, callback):
        if self.THREAD == None or not self.THREAD.is_alive():
            self.THREAD = threading.Thread(target=self.daemon_work, args=[callback], daemon=True)
        self.THREAD.start()

    def shutdown(self):
        logger.info("Job-schedule shutdown")
        self.SHUT_DOWN = True
