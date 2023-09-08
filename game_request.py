from datetime import datetime

class game_request:
    def __init__(self,ip:str,user:str,timestamp=datetime.now()):
        self.ip=ip
        self.user=user
        self.timestamp=timestamp
    #this will break if attr names change
    def load_from_dict(self,ob):
        self.ip=ob['ip']
        self.user=ob['user']
        self.timestamp=ob['timestamp']