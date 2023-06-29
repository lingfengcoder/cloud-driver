
class TbTaskPo:
    id:int
    config_id:int
    sync_src:str
    sync_dest:str
    type:int
    schedule:str
    state:int
    def __init__(self,config_id,sync_src,sync_dest,type,schedule,state):
        self.type=type
        self.config_id=config_id
        self.sync_src=sync_src
        self.sync_dest=sync_dest
        self.schedule=schedule
        self.state=state