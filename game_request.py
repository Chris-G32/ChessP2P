from datetime import datetime,date



class game_request:
    def __init__(self,ip:str,user="",timestamp=datetime.now()):
        self.ip=ip
        self.user=user
        self.timestamp=timestamp
    #this will break if attr names change
    def load_from_dict(self,ob):
        self.ip=ob['ip']
        self.user=ob['user']
        self.timestamp=ob['timestamp']
    def serialize(self):
        pass
    def deserialize(self):
        pass