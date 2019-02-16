import json
from last_data import lastData
from actions import Actions
from manage_firbebase import ManageFirebase


class Data:
    def __init__(self):
        self.pastData = lastData()
        self.pastData.init(0.0, 0, False, False)
        self.firebaseObj = ManageFirebase()

    def msgToSend(self, msg):
        return json.dumps(msg).encode('utf-8')

    def msgRecieved(self, msg):
        return json.loads(msg)

    def isChanged(self, data):
        if(data['action'] == Actions.SENSOR_INFO.value):
            newData = lastData()
            newData.fromJson(data)
            if(self.pastData.temp != newData.temp):
                print('Temp')
                print(newData.temp)
                self.firebaseObj.addSensorData({u'temp': newData.temp})
                self.pastData.temp = newData.temp
            if(self.pastData.humidity != newData.humidity):
                print('Humidity')
                print(newData.humidity)
                self.firebaseObj.addSensorData({u'humidity': newData.humidity})
                self.pastData.humidity = newData.humidity
            if(self.pastData.rain != newData.rain):
                print('Rain')
                print(newData.rain)
                self.firebaseObj.addSensorData({u'rain': newData.rain})
                self.pastData.rain = newData.rain
            if(self.pastData.cloud != newData.cloud):
                print('Cloud')
                print(newData.cloud)
                self.firebaseObj.addSensorData({u'cloud': newData.cloud})
                self.pastData.cloud = newData.cloud
