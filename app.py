from flask import Flask, render_template, request
from firestore_utils import add_expense
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
    return "Expense added successfully!"

if __name__ == "__main__":
    app.run(debug=True)
