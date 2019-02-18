import json
from device_data import DeviceData
from actions import Actions


class Receiver:
    def __init__(self, serial_port, db):
        self.serial_port = serial_port
        self.db = db
        self.current_data = DeviceData()
        doc_ref = self.db.collection(u'home').document(u'devices')
        self.doc_watch = doc_ref.on_snapshot(self.device_data)

    def send_data(self, data):
        self.serial_port.write(self.msg_to_send(data))

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def device_data(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            self.process_data(doc.to_dict())

    def process_data(self, data):
        if data['light'] != self.current_data.led:
            temp = {u'action': Actions.LED.value, u'value': data['light']}
            self.send_data(temp)
            self.current_data.led = data['light']
        if data['fan'] != self.current_data.led:
            temp = {u'action': Actions.FAN.value, u'value': data['fan']}
            self.send_data(temp)
            self.current_data.led = data['fan']
