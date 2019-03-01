from pad4pi import rpi_gpio
import sys
import json
from uno_actions import unoActions
from subprocess import call

class Local:
    def __init__(self, uno, db):
        KEYPAD = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ["*", 0, "#", "D"]
        ]
        ROW_PINS = [4, 17, 27, 22] # BCM numbering
        COL_PINS = [5, 6, 13, 19] # BCM numbering
        self.uno = uno
        self.db = db
        self.password = ""
        factory = rpi_gpio.KeypadFactory()
        # Try factory.create_4_by_3_keypad
        # and factory.create_4_by_4_keypad for reasonable defaults
        self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
        self.keypad.registerKeyPressHandler(self.keyPressed)

    def keyPressed(self, key):
        if(key == "A"):
            print(self.password)
            self.password = ""
        elif(key == "B"):
            call("sudo reboot -h now", shell=True)
        elif(key == "C"):
            call("sudo shutdown -h now", shell=True)
        elif(key == "D"):
            self.keypad.cleanup()
            self.send_data({u'action': unoActions.LED1.value, u'value': 0})
            self.send_data({u'action': unoActions.LED2.value, u'value': 0})
            self.send_data({u'action': unoActions.FAN.value, u'value': 0})
            self.send_data({u'action': unoActions.DOOR.value, u'state': False})
            self.send_data({u'action': unoActions.BUZZ.value, u'state': False})
            self.add_device_data({u'light1': 0, u'light2': 0, u'fan': 0, u'door': False})
            sys.exit()
        else:
            self.password += key

    def send_data(self, data):
        self.uno.write(self.msg_to_send(data))

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def add_device_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'devices')
        doc_ref.update(data)
