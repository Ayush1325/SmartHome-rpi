import firebase_admin
from firebase_admin import firestore


class ManageFirebase:
    def __init__(self):
        cred = firebase_admin.credentials.Certificate(
            "smarthome-ee796-firebase-adminsdk-e5uty-d2e5e8672e.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_sensor_data(self, data):
        docRef = self.db.collection(u'home').document(u'weather')
        docRef.update(data)

    def init_listener(self, data):
        docRef = self.db.collection(u'home').document(u'devices')
