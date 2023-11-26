from typing import Any

from pydantic.dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class TbConfigPo(BaseModel):
    id: int
    type: int
    host: str
    username: str
    password: str

    def __init__(self,id, type, host, username, password,**kwargs):
        super().__init__(id=id,type=type,host=host,username=username,password=password)
        self.id=id
        self.type = type
        self.host = host
        self.username = username
        self.password = password
