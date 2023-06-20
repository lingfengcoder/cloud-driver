import time

from webdav3.client import Client
import os
from log import logger
import HttpUtil
import threading
import random
from concurrent.futures import ThreadPoolExecutor
from Schedule import schedule

#
SRC_PATH="/alist/下载"
TAR_PATH="/mnt/user/movie/"

options = {
    'webdav_hostname': "http://ip:port/dav",
    'webdav_login': "user",
    'webdav_password': "pwd",
    "disable_check": True,
}

client = Client(options)
client.verify = False


# dev前缀
DAV = "/dav/"
# 最多任务数
MAX_TASK_NUM = 3
# 当前任务数
CURR_TASK_NUM = 0
# 多线程安全锁
MUTEX = threading.Lock()
# 暂停信号
PAUSE = True
# 执行任务列表
TASK_LIST = []
# 线程池
pool = ThreadPoolExecutor(max_workers=50)

# 任务数+1
def add_task(task):
    global TASK_LIST
    if len(TASK_LIST) < MAX_TASK_NUM:
        MUTEX.acquire()
        if len(TASK_LIST) < MAX_TASK_NUM:
            TASK_LIST.append(task)
            MUTEX.release()
            return True
        else:
            MUTEX.release()
    return False


# 任务数-1
def reduce_task(task):
    global CURR_TASK_NUM
    MUTEX.acquire()
    TASK_LIST.remove(task)
    MUTEX.release()
    return True


def print_list(list: []):
    for i in list:
        logger.info(i.tostring())


def submit_task(task):
    global TASK_LIST
    count = 0
    while 1:
        count += 1
        if TASK_LIST != None and len(TASK_LIST) > 0:
            print_list(TASK_LIST)
        logger.info("第%s此尝试: %s" % (count, task.remote_path))
        if add_task(task):
            time.sleep(random.randint(1, HttpUtil.SPEED_LIMIT_TIME))
            pool.submit(sync, task)
            break
        else:
            time.sleep(5)

def process(current, total, task):
    task.local_size = current
    task.progress = round((current / total) * 100, 2)
    # logger.info(f" current={current}- total={total}")


def complete(task):
    # 任务数-1
    reduce_task(task)
    if not PAUSE:
        logger.info("%s 下载完成" % task.remote_path)


def sync(task):
    if task.local_size == 0:
        logger.info("开始下载 %s %s" % (task.remote_path, task.local_path))
    else:
        logger.info(f"开始断点续传:%s %s {task.local_size}-{task.remote_size}" % (task.remote_path, task.local_size))

    HttpUtil.append_file(_client=client, remote_path=task.remote_path, remote_size=task.remote_size,
                         local_size=task.local_size,
                         local_path=task.local_path, progress=process, progress_args={task})
    # progress_args=task
    complete(task)


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
        return f"remote_path={self.remote_path} local_path={self.local_path} progress={self.progress} local_size={self.local_size} remote_size={self.remote_size}"


def list(path, local):
    if PAUSE:
        logger.info("暂停任务")
        return
    logger.info("list:%s" % path)
    files = client.list(path, True)

    for item in files[1:]:
        if PAUSE:
            logger.info("暂停任务")
            return
        remote_file = item['path'].removeprefix(DAV)
        if item['isdir']:
            # 递归处理
            local_file = local + remote_file
            if not os.path.exists(local_file):
                os.makedirs(local_file)
            list(remote_file, local)
        else:
            logger.info("开始检测file:%s" % remote_file)
            local_file = local + remote_file
            if os.path.exists(local_file):
                if os.path.isfile(local_file):
                    file_len = os.path.getsize(local + remote_file)
                    # 远程文件和本地文件大小不一致，则进行下载
                    remote_size = int(item['size'])
                    if file_len < remote_size:
                        submit_task(Task(remote_file, local_file, remote_size, file_len))
                    else:
                        logger.info("%s 已经下载完毕" % (remote_file))
                else:
                    logger.info("检测是文件夹%s" % local_file)
                    # os.remove(local_file)
                    submit_task(Task(remote_file, local_file))
            else:
                submit_task(Task(remote_file, local_file))


def stop():
    logger.info("暂停同步")
    global PAUSE
    PAUSE = True
    HttpUtil.STOP = True


def start():
    logger.info("开始同步")
    global PAUSE
    global TASK_LIST
    PAUSE = False
    HttpUtil.STOP = False
    TASK_LIST=[]
    # TASK_LIST.clear()
    list(SRC_PATH,TAR_PATH)



def schedule_callback(enable):
    # logger.info("schedule_callback " , (param))
    if enable:
        if PAUSE:
            threading.Thread(target=start).start()
    else:
        stop()


if __name__ == '__main__':
    schedule.schedule(callback=schedule_callback)
    while 1:
        time.sleep(100)
    # list("/aliyun_share", "F:/download/")
    # download("alist/", "F:/download/")
