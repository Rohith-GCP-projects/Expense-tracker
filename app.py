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

if __name__ == "__main__":
    app.run(debug=True)
