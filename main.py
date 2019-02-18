from serial_helper import SerialHelper
from actions import Actions


serialObj = SerialHelper()

while True:
    temp = {'action': Actions.SENSOR_INFO.value}
    serialObj.send_data(temp)
    serialObj.read_data()
