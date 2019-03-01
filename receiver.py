import json
from device_data import DeviceData
from subprocess import call
from uno_actions import unoActions


class Receiver:
    def __init__(self, serial_port, db):
        self.serial_port = serial_port
        self.db = db
        self.current_data = DeviceData()
        doc_ref = self.db.collection(u'home').document(u'devices')
        self.doc_watch = doc_ref.on_snapshot(self.device_data)
        doc_ref2 = self.db.collection(u'home').document(u'rpiControls')
        self.doc_watch2 = doc_ref2.on_snapshot(self.shutdown)

    def send_data(self, data):
        self.serial_port.write(self.msg_to_send(data))

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def device_data(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            self.process_data(doc.to_dict())

    def shutdown(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            data = doc.to_dict()
            if(data['powerOff']):
                self.db.collection(u'home').document(u'rpiControls').update({'powerOff': False})
                call("sudo shutdown -h now", shell=True)

    def process_data(self, data):
        if data['light1'] != self.current_data.led1:
            temp = {u'action': unoActions.LED1.value, u'value': data['light1']}
            self.send_data(temp)
            self.current_data.led1 = data['light1']
        if data['light2'] != self.current_data.led2:
            temp = {u'action': unoActions.LED2.value, u'value': data['light2']}
            self.send_data(temp)
            self.current_data.led2 = data['light2']
        if data['fan'] != self.current_data.fan:
            temp = {u'action': unoActions.FAN.value, u'value': data['fan']}
            self.send_data(temp)
            self.current_data.fan = data['fan']
        if data['door'] != self.current_data.door:
            temp = {u'action': unoActions.DOOR.value, u'state': data['door']}
            self.send_data(temp)
            self.current_data.door = data['door']
