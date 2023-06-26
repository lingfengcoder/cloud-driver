
class WebDavConfig:

    base={
        "sync_src":"",
        "sync_dest":""
    }

    options = {
        'webdav_hostname': "",
        'webdav_login': "",
        'webdav_password': "",
        "disable_check": True,
    }
    def __init__(self,option,base):
       self.options=option
       self.base=base