from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("firebase-key.json")
default_app = initialize_app(cred)

db = firestore.client()

def add_expense(data):
    return db.collection("expenses").add(data)

def get_expenses():
    return [ {**doc.to_dict(), "id": doc.id} for doc in db.collection("expenses").stream() ]
