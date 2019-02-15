import json


class Data:
    def msgToSend(self, msg):
        return json.dumps(msg).encode('utf-8')

    def msgRecieved(self, msg):
        return json.loads(msg)
