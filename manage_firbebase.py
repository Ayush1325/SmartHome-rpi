import firebase_admin
from firebase_admin import firestore


class ManageFirebase:
    def __init__(self):
        cred = firebase_admin.credentials.Certificate(
            "smarthome-ee796-firebase-adminsdk-e5uty-d2e5e8672e.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def addSensorData(self, data):
        docRef = self.db.collection(u'home').document(u'sensors')
        docRef.update(data)
