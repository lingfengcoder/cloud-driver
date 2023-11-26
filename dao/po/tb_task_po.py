from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from datetime import datetime


@dataclass
class TbTaskPo(BaseModel):
    id: int
    config_id: int
    sync_src: str
    sync_dest: str
    type: int
    schedule: str
    state: int
    update_time: datetime = None

    # def __init__(self, dictionary):
    #     for key in dictionary:
    #       setattr(self, key, dictionary[key])
    def __init__(self, id, config_id, sync_src, sync_dest, type, schedule, state, update_time, **kwargs):
        super().__init__(config_id=config_id, id=id, sync_src=sync_src, sync_dest=sync_dest, type=type,
                         schedule=schedule,
                         state=state)
        self.type = type
        self.id = id
        self.config_id = config_id
        self.sync_src = sync_src
        self.sync_dest = sync_dest
        self.schedule = schedule
        self.state = state
        self.update_time = update_time
