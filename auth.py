# auth.py
import firebase_admin
from firebase_admin import credentials, auth

# initialize once
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

def verify_id_token(id_token):
    """
    Returns decoded token dict on success, or raises an exception on failure.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded
