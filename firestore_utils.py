# firestore_utils.py
from google.cloud import firestore

db = firestore.Client()  # uses firebase-key.json credentials via GOOGLE_APPLICATION_CREDENTIALS or service account

EXPENSES_COLLECTION = "expenses"  # each doc: userId => subcollection or store userId field

def add_expense(user_id, amount, category, date, note=""):
    doc_ref = db.collection(EXPENSES_COLLECTION).document()
    data = {
        "user_id": user_id,
        "amount": float(amount),
        "category": category,
        "date": date,   # ISO string recommended: "2025-11-05"
        "note": note,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    doc_ref.set(data)
    return doc_ref.id

def get_expenses_for_user(user_id, limit=100):
    q = (
        db.collection(EXPENSES_COLLECTION)
          .where("user_id", "==", user_id)
          .order_by("created_at", direction=firestore.Query.DESCENDING)
          .limit(limit)
    )
    docs = q.stream()
    results = []
    for d in docs:
        r = d.to_dict()
        r["id"] = d.id
        results.append(r)
    return results
