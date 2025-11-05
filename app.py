# app.py
from flask import Flask, request, jsonify
from auth import verify_id_token
import firestore_utils as dbu

app = Flask(__name__)

def get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]
    return None

@app.route("/")
def home():
    return jsonify({"message": "Expense Tracker running"})

@app.route("/add_expense", methods=["POST"])
def add_expense():
    token = get_bearer_token()
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401
    try:
        decoded = verify_id_token(token)
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401

    payload = request.json or {}
    required = ("amount", "category", "date")
    if not all(k in payload for k in required):
        return jsonify({"error": "Missing fields: amount, category, date required"}), 400

    uid = decoded["uid"]
    doc_id = dbu.add_expense(
        user_id=uid,
        amount=payload["amount"],
        category=payload["category"],
        date=payload["date"],
        note=payload.get("note", "")
    )
    return jsonify({"success": True, "id": doc_id}), 201

@app.route("/expenses", methods=["GET"])
def get_expenses():
    token = get_bearer_token()
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401
    try:
        decoded = verify_id_token(token)
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401

    uid = decoded["uid"]
    results = dbu.get_expenses_for_user(uid)
    return jsonify({"expenses": results})

if __name__ == "__main__":
    app.run(debug=True)
