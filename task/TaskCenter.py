from sdk.WebDav import WebDav
from sdk.Config import WebDavConfig
from sdk.log import logger

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

map = {}


def new_task():
    # 任务需要去重
    config = WebDavConfig(options, base)
    webdav = WebDav(config=config)
    webdav.start()
    map[str(webdav.__hash__())] = {'config': config, 'webdav': webdav}
    return True


# 获取任务列表
def task_list():
    result = {}
    for k in map:
        result[k] = map[k]['config']
    return result


# 停止任务（包括定时器）
def stop_task(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.stop()
        return True
    logger.error("任务不存在task_id: %s" % task_id)
    return False


# 继续任务
def restart_task(task_id):
    item = map.get(task_id)
    if item != None:
        webdav = item['webdav']
        webdav.start()
    return True


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
