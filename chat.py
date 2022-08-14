
class Chat:
    chatid = 0
    minlenght = 0
    isrecognize = 0

    def __init__(self, _id, _l, _r):
        self.chatid = _id
        self.isrecognize = _r
        self.minlenght = _l
