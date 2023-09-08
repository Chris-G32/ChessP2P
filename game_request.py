from datetime import datetime

class game_request:
    def __init__(self,ip,user):
        self.ip=ip
        self.user=user
        self.timestamp=datetime.now()
    