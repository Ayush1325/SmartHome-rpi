import serial
import firebase_admin
from firebase_admin import firestore
from sender import Sender
from receiver import Receiver
from local import Local
from device_data import DeviceData

# serial_port = serial.Serial("/dev/ttyACM0", 9600)

uno = serial.Serial("/dev/ttyACM0", 9600)
nano = serial.Serial("/dev/ttyUSB0", 9600)

data = DeviceData()

cred = firebase_admin.credentials.Certificate("smarthome-ee796-firebase-adminsdk-e5uty-d2e5e8672e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

localObj = Local(uno, db)
sender_obj = Sender(uno, nano, db, data)
receiver_obj = Receiver(uno, db, data)

sender_obj.start_loop()
