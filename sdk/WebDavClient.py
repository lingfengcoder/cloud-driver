
from webdav3.client import Client
from sdk.Config import WebDavConfig

def get_webdav3_client(config:WebDavConfig)->Client:
    client = Client(config)
    client.verify = False
    return client