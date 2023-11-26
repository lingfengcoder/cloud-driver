from sdk.WebDav import WebDav
from sdk.Config import WebDavConfig
from sdk.log import logger
from dao.po.tb_task_po import TbTaskPo
from dao.po.tb_config_po import TbConfigPo
import json
from sdk.WebDav import TASK_STATE

base = {
    "sync_src": "/alist/下载",
    "sync_dest": "/mnt/user/movie/"
}

base2 = {
    "sync_src": "/alist/movie",
    "sync_dest": "/mnt/user/movie2/"
}

options = {
    'webdav_hostname': "http://192.168.3.26:5244/dav",
    'webdav_login': "lf",
    'webdav_password': "pwd",
    "disable_check": True,
}
# 运行时任务列表
map = {}


def new_task(task: TbTaskPo, config: TbConfigPo, lastUpdateTime):
    # 任务需要去重
    options = {
        'webdav_hostname': config.host,
        'webdav_login': config.username,
        'webdav_password': config.password,
        "disable_check": True,
    }

    base = {
        "id": task.id,
        "sync_src": task.sync_src,
        "sync_dest": task.sync_dest,
        # json序列化task.schedule成字典
        "schedule": json.loads(task.schedule)
    }
    config = WebDavConfig(options, base, lastUpdateTime)
    webdav = WebDav(config=config)
    webdav.start()
    map[task.id] = {'config': config, 'webdav': webdav}
    return True


# 获取任务列表
def task_list():
    result = {}
    for k in map:
        result[k] = map[k]['config']
    return result


# 获取其中一个任务
def get_taskConfig(task_id):
    item = map.get(task_id)
    if item != None:
        return item['config']
    return None


def update_schedule(task_id, schedule, lastUpdateTime):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.update_schedule(schedule)
        item['config'].lastUpdateTime = lastUpdateTime
        return True
    return False


# 停止任务（包括定时器）
def stop_task(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.stop()
        return True
    # logger.error("任务不存在task_id: %s" % task_id)
    return False
#删除任务
def delete_task(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.shutdown()
        del map[task_id]
        return True
    # logger.error("任务不存在task_id: %s" % task_id)
    return False

# 继续任务
def restart_task(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.restart()
    return True


def is_task_error(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        return webdav.STATE == TASK_STATE.ERROR
    return None
#任务是否暂停
def is_task_pause(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        return webdav.PAUSE
    return None

# 获取任务进度
def get_task_process(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        return webdav.TASK_LIST
    return None


# 将所有的任务都关闭
def shutdown(who):
    for k in map:
        webdav = map[k]['webdav']
        if webdav != None:
            logger.info("who call shutdown=%s" % who)
            webdav.shutdown()
