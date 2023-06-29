from typing import Any

from pydantic.dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class TbConfigPo(BaseModel):
    id: int | None = None
    type: int
    host: str
    username: str
    password: str

    def __init__(self, type, host, username, password):
        super().__init__(type=type,host=host,username=username,password=password)
        self.type = type
        self.host = host
        self.username = username
        self.password = password
