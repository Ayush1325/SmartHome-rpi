import serial
import firebase_admin
from firebase_admin import firestore
from sender import Sender
from receiver import Receiver

# serial_port = serial.Serial("/dev/ttyACM0", 9600)

uno = serial.Serial("/dev/ttyACM0", 9600)
nano = serial.Serial("/dev/ttyUSB0", 9600)

cred = firebase_admin.credentials.Certificate("smarthome-ee796-firebase-adminsdk-e5uty-d2e5e8672e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

sender_obj = Sender(uno, nano, db)
receiver_obj = Receiver(uno, db)

sender_obj.start_loop()
