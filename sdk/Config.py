class WebDavConfig:
    base = {
        "sync_src": "",
        "sync_dest": "",
        "schedule": ""
    }

    options = {
        'webdav_hostname': "",
        'webdav_login': "",
        'webdav_password': "",
        "disable_check": True,
    }
    # 上次更新的时间 0代表仅仅初始化没有任何更新
    lastUpdateTime = 0

    def __init__(self, option, base, lastUpdateTime):
        self.options = option
        self.base = base
        self.lastUpdateTime = lastUpdateTime
