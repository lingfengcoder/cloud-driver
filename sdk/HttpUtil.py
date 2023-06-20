import os
from log import logger
from webdav3.exceptions import RemoteResourceNotFound, OptionNotValid
from webdav3.urn import Urn
import time


SPEED_LIMIT_SIZE=7*1024*1024
SPEED_LIMIT_TIME=3
STOP=False

def append_file(_client, remote_path, local_path,remote_size=0, local_size=0, progress=None, progress_args=()):
    if STOP:
        logger.info("%s stop signal" % (remote_path))
        return
    block_size = 10 * 1024 * 1024
    urn = Urn(remote_path)
    if _client.is_dir(urn.path()):
        raise OptionNotValid(name="remote_path", value=remote_path)

    if os.path.isdir(local_path):
        raise OptionNotValid(name="local_path", value=local_path)

    if not _client.check(urn.path()):
        raise RemoteResourceNotFound(urn.path())
    _client.chunk_size=1500
    with open(local_path, 'ab')  as local_file:
        # append("Range:" + f"bytes={local_size}-{remote_size}")
        # response = _client.execute_request('download', urn.quote(),headers_ext=["Range:" + f"bytes={local_size}-{remote_size}"])
        response = _client.execute_request('download', urn.quote(),headers_ext=["Range:" + f"bytes={local_size}-"])
        total = int(response.headers['content-length'])
        total=remote_size if total<remote_size else total
        current = local_size
        if callable(progress):
            progress(current, total, *progress_args)  # zero call
        buff = 0
        speendLimit = SpeedLimit(0, _client.chunk_size, 0, 0)
        for block in response.iter_content(chunk_size=_client.chunk_size):
            buff += _client.chunk_size
            local_file.write(block)
            # 刷新释放内存
            if buff >= block_size:
                local_file.flush()
                buff = 0
                if callable(progress):
                    progress(current, total, *progress_args)
            current += _client.chunk_size
            #限速
            speed_limit(_client.chunk_size,SPEED_LIMIT_SIZE,SPEED_LIMIT_TIME,speendLimit)
            if STOP:
              logger.info("%s stop signal"%(remote_path))
              return
# 限速
#在speed_limit_time 这个单位时间内下载量不能超过 speed_limit_size 限速为 speed_limit_size/speed_limit_time(B/s)
def speed_limit(increment,speed_limit_size,speed_limit_time, speed_limit):
    #从开始下载开始累计下载量
    speed_limit.download_size+=increment
    #上次限速时，下载的量
    speed_last_download_size = speed_limit.speed_last_download_size
    #上次限速时的时间
    speed_limit_last_time = speed_limit.speed_limit_last_time
    #  当前下载量，对比上次限速时的量，增量如果超过限制
    if (speed_limit.download_size - speed_last_download_size >= speed_limit_size):
        #看从上次限速到本次间隔多久
        interval =(time.time() - speed_limit_last_time)
        # 间隔时间小于单位时间，等待剩余的时间
        if (interval < speed_limit_time):
            t=round(speed_limit_time - interval,2)
            logger.info("sleep:%s s"%t)
            time.sleep(t)
        speed_limit.speed_last_download_size = speed_limit.download_size
        speed_limit.speed_limit_last_time = time.time()

#限速对象
class SpeedLimit:
    download_size:0
    increment:0
    speed_last_download_size:0
    speed_limit_last_time:0
    def __init__(self, download_size,increment,speed_last_download_size,speed_limit_last_time):
        self.download_size=download_size
        self.increment=increment
        self.speed_limit_last_time=speed_limit_last_time
        self.speed_last_download_size=speed_last_download_size
