# GCP Expense Tracker
This is the RGCP Expense Tracker, a lightweight Flask app that logs expenses to Firestore and serves both the input form and the ledger via `rohithshan.nidhushan.com`.

## Features
- Add a new expense with a reason, amount, and optional timestamp.
- View every submission on the anime-inspired ledger page.
- Styled with a black-and-grey “classic anime” aesthetic for both form and report views.

## Deployment
The live version is hosted at `rohithshan.nidhushan.com`. For local development:

1. Install dependencies from `requirements.txt`.
2. Place your Firebase service account key in `firebase-key.json`.
3. Run `FLASK_APP=app.py flask run` (or `python app.py`) and open `http://localhost:5000`.

## Structure
- `app.py` defines the Flask routes for submitting and viewing expenses.
- `firestore_utils.py` handles Firestore connectivity and data access.
- `templates/` contains the stylized `form.html` and `expenses.html` pages.
