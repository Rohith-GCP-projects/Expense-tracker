<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
from firestore_utils import add_expense, get_expenses
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    amount = request.form.get("amount")
    reason = request.form.get("reason")
    date = request.form.get("date")

    # If user didn’t pick date → use today
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    data = {
        "amount": float(amount),
        "reason": reason,
        "date": date
    }

    add_expense(data)
    return redirect("/")
    # return """
    #     <h3>Expense logged successfully!</h3>
    #     <a href="/">Go Back</a>
    #     """

@app.route("/get_expenses", methods=["GET"])
def fetch_expenses():
    try:
        expense_list = get_expenses()
        return render_template("expenses.html", expenses=expense_list)
    except Exception as e:
        return f"Error: {e}"
=======
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
>>>>>>> 9acf17692090aea8014789d866f26ac826875a68

if __name__ == "__main__":
    app.run(debug=True)
