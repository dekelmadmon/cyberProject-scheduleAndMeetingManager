class Meeting:
    def __init__(self,
        requester,
        reciever,
        date,
        status):
        self.requester = requester
        self.reciever = reciever
        self.date = date
        self.status = status