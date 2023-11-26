import time

import os
import random
import threading
from sdk.log import logger
from sdk.HttpUtil import HttpUtil
from concurrent.futures import ThreadPoolExecutor
from sdk.Schedule import Schedule
from sdk.Config import WebDavConfig
from sdk.WebDavClient import get_webdav3_client


class TASK_STATE:
    ERROR = -1
    WAIT = 0
    RUN = 1
    FINISHED = 2


class WebDav:
    # dev前缀
    DAV = "/dav"

    def __init__(self, config: WebDavConfig):
        self.config = config
        # webDav的客户端
        self.client = get_webdav3_client(config.options)
        # 定时任务
        self.schedule = Schedule(config.base['schedule'])
        # 最多任务数
        self.MAX_TASK_NUM = 3
        # 多线程安全锁
        self.MUTEX = threading.Lock()
        # 暂停信号
        self.PAUSE = True
        # 彻底关闭信号
        self.SHUT_DOWN = False
        # 任务状态
        self.STATE = 0
        # 执行任务列表
        self.TASK_LIST = []
        # 线程池
        self.pool = ThreadPoolExecutor(max_workers=50)
        # http
        self.http = HttpUtil()

    # 任务数+1
    def add_task(self, task):
        if len(self.TASK_LIST) < self.MAX_TASK_NUM:
            self.MUTEX.acquire()
            if len(self.TASK_LIST) < self.MAX_TASK_NUM:
                self.TASK_LIST.append(task)
                self.MUTEX.release()
                return True
            else:
                self.MUTEX.release()
        return False

    # 任务数-1
    def reduce_task(self, task):
        self.MUTEX.acquire()
        self.TASK_LIST.remove(task)
        self.MUTEX.release()
        return True

    # 打印当前任务队列信息
    def print_list(self, list: []):
        for i in list:
            logger.info(i.simple_tostr())

    # 提交下载任务，此处会阻塞list方法中的线程，并不断尝试加入任务队列
    def submit_task(self, task):
        count = 0
        while 1:
            if self.PAUSE: break
            count += 1
            if self.TASK_LIST != None and len(self.TASK_LIST) > 0:
                self.print_list(self.TASK_LIST)
            logger.info("第%s此尝试: %s" % (count, task.remote_path))
            if self.add_task(task):
                time.sleep(random.randint(1, self.http.SPEED_LIMIT_TIME))
                self.pool.submit(self.sync, task)
                break
            else:
                time.sleep(5)

    # 下载进度的回调
    def process(self, current, total, task):
        task.local_size = current
        task.progress = round((current / total) * 100, 2)
        # logger.info(f" current={current}- total={total}")

    # 下载任务完成的通知
    def complete(self, task):
        # 任务数-1
        self.reduce_task(task)
        if not self.PAUSE:
            logger.info("%s 下载完成" % task.remote_path)

    # 将远程的文件同步到本地，支持断点续传
    def sync(self, task):
        if task.local_size == 0:
            logger.info("开始下载 %s %s" % (task.remote_path, task.local_path))
        else:
            logger.info(
                f"开始断点续传:%s %s {task.local_size}-{task.remote_size}" % (task.remote_path, task.local_size))

        self.http.append_file(_client=self.client, remote_path=task.remote_path, remote_size=task.remote_size,
                              local_size=task.local_size,
                              local_path=task.local_path, progress=self.process, progress_args={task})
        self.complete(task)

    # 内部下载任务
    class Task:
        remote_path: str
        local_path: str
        remote_size: 0
        local_size: 0
        progress: 0

        def __init__(self, remote_path, local_path, remote_size=0, local_size=0, progress=0):
            self.remote_path = remote_path
            self.local_path = local_path
            self.remote_size = remote_size
            self.local_size = local_size
            self.progress = progress

        def tostring(self):
            return f"remote_path={self.remote_path} local_path={self.local_path} progress={self.progress}% local_size={self.local_size} remote_size={self.remote_size}"

        def simple_tostr(self):
            return f"remote_path={self.remote_path}  progress={self.progress}% "

    # 扫描远程目录与本地目录进行对比
    # 1.创建缺失的目录 2.下载缺失的文件
    def list(self, path: str, local: str):
        try:
            # path = path if path.endswith("/") else path + "/"
            # prefix = self.DAV + path
            # logger.info("list prefix=%s" % prefix)
            if self.PAUSE:
                logger.info("list stop任务")
                return
            logger.info("list: %s" % path)
            files = self.client.list(path, True)
            for item in files[1:]:
                if self.PAUSE:
                    logger.info("list stop任务")
                    return
                    remote_file = item['path'].removeprefix(self.DAV + "/")
                    if item['isdir']:
                        # 递归处理
                        local_file = local + remote_file
                        if not os.path.exists(local_file):
                            os.makedirs(local_file)
                        self.list(remote_file, local)
                    else:
                        logger.info("开始检测file:%s" % remote_file)
                        local_file = local + remote_file
                        if os.path.exists(local_file):
                            if os.path.isfile(local_file):
                                file_len = os.path.getsize(local + remote_file)
                                # 远程文件和本地文件大小不一致，则进行下载
                                remote_size = int(item['size'])
                                if file_len < remote_size:
                                    self.submit_task(self.Task(remote_file, local_file, remote_size, file_len))
                                else:
                                    logger.info("%s 已经下载完毕" % (remote_file))
                            else:
                                logger.info("检测是文件夹%s" % local_file)
                                # os.remove(local_file)
                                self.submit_task(self.Task(remote_file, local_file))
                        else:
                            self.submit_task(self.Task(remote_file, local_file))
        except Exception as err:
            logger.error("list err=%s msg:%s" % (err.__class__, err))
            self.shutdown()
            self.STATE = TASK_STATE.ERROR

    # 定时任务的回调
    def schedule_callback(self, enable):
        if enable:
            # 如果现在是暂停的状态，则可以开始
            if self.PAUSE:
                self.restart()
        else:
            self.pause()

    def pause(self):
        # 设置停止标志位
        self.PAUSE = True
        # 暂停http
        self.http.stop()

    # 真正的任务开始点
    def restart(self):
        logger.info("开始同步")
        # 取消停止
        self.PAUSE = False
        # http开启
        self.http.start()
        # 清空任务队列
        self.TASK_LIST.clear()
        # 开启新线程进行任务
        threading.Thread(target=self.list, args=(self.config.base['sync_src'], self.config.base['sync_dest']),
                         daemon=True).start()

    # 开始的入口
    def start(self):
        # 启动定时任务
        if self.schedule == None:
            # self.init_schedule(schedule=None)
            logger.error("schedule is None,can not run job")
        else:
            self.schedule.time_work(callback=self.schedule_callback)

    # 更新定时任务
    def update_schedule(self, schedule):
        self.shutdown()
        self.schedule = Schedule(schedule)
        self.start()

    # 停止工作
    def stop(self):
        self.pause()
        # 定时任务关闭
        self.schedule.shutdown()
        # 清除定时器
        # self.schedule = None

    # 彻底关机
    def shutdown(self):
        logger.info("WebDav shutdown")
        self.SHUT_DOWN = True
        # 停止标志
        self.stop()
        # 关闭线程池
        self.pool.shutdown(wait=False, cancel_futures=True)

    #
    def test(self):
        logger.info("test")
        try:
            self.client.check("/")
            return True
        except Exception as e:
            logger.error(e)
        return False


def test(config: WebDavConfig):
    try:
        client = get_webdav3_client(config.options)
        data = client.info("/")
        logger.info("test:%s" % data)
        return True
    except Exception as e:
        logger.error(e)
    return False


if __name__ == '__main__':
    base = {
        "sync_src": "/alist/下载",
        "sync_dest": "/mnt/user/movie/"
    }
    options = {
        'webdav_hostname': "http://192.168.3.26:5244/dav",
        'webdav_login': "lingfeng",
        'webdav_password': "wz@14031424",
        "disable_check": True,
    }
    config = WebDavConfig(options, base)
    webdav = WebDav(config=config)
    webdav.start()
    while 1:
        time.sleep(100)

    # list("/aliyun_share", "F:/download/")
    # download("alist/", "F:/download/")
