from flask import Flask, render_template, request, redirect, jsonify, url_for
from bank import BankAccount, accounts, create_account, deposit_to_account, withdraw_from_account, check_balance, delete_user
import db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account_route():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        acc_type = request.form['account_type']
        balance = float(request.form['initial_balance'])
        new_account = BankAccount(first, last, acc_type, balance, email)
        accounts[new_account.account_no] = new_account
        db.insert_users(first, last, email)
        db.insert_accounts(new_account.user_id, new_account.account_no, new_account.account_type, new_account.balance)
        return render_template('success.html', message="Account created successfully!", data=new_account)
    return render_template('create_account.html')
#deposit
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'GET':
        return render_template('deposit.html')

    # Check if it's a JSON request (API call)
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        account_number = data.get('account_number')
        amount = data.get('amount')

        matched_account = None

        if email:
            for acc in accounts.values():
                if acc.email == email:
                    matched_account = acc
                    break

        if not matched_account and account_number:
            for acc in accounts.values():
                if acc.account_no == account_number:
                    matched_account = acc
                    break

        if not matched_account:
            return jsonify({'status': 'error', 'message': 'Account not found.'}), 404

        if matched_account.account_no != account_number:
            return jsonify({'status': 'error', 'message': 'Email and account number do not match.'}), 400

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Invalid deposit amount.'}), 400

        matched_account.balance += amount
        db.update_balance(matched_account.user_id, matched_account.balance)

        return jsonify({
            'status': 'success',
            'message': f'Deposit of ₹{amount} successful.',
            'data': {
                'first_name': matched_account.first_name,
                'last_name': matched_account.last_name,
                'email': matched_account.email,
                'account_no': matched_account.account_no,
                'account_type': matched_account.account_type,
                'balance': matched_account.balance
            }
        }), 200

    # Form-based HTML POST handling (optional fallback)
    else:
        return render_template('success.html', message="Form-based deposit not implemented.")


#withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'GET':
        return render_template('withdraw.html')

    # JSON-based API POST request
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        account_number = data.get('account_number')
        amount = data.get('amount')

        matched_account = None

        # Try to find account by email
        if email:
            for acc in accounts.values():
                if acc.email == email:
                    matched_account = acc
                    break

        # Try fallback match by account number
        if not matched_account and account_number:
            for acc in accounts.values():
                if acc.account_no == account_number:
                    matched_account = acc
                    break

        if not matched_account:
            return jsonify({'status': 'error', 'message': 'Account not found.'}), 404

        if matched_account.account_no != account_number:
            return jsonify({'status': 'error', 'message': 'Email and account number do not match.'}), 400

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Invalid withdrawal amount.'}), 400

        if matched_account.balance < amount:
            return jsonify({'status': 'error', 'message': 'Insufficient balance.'}), 400

        matched_account.balance -= amount
        db.update_balance(matched_account.user_id, matched_account.balance)

        return jsonify({
            'status': 'success',
            'message': f'Withdrawal of ₹{amount} successful.',
            'data': {
                'first_name': matched_account.first_name,
                'last_name': matched_account.last_name,
                'email': matched_account.email,
                'account_no': matched_account.account_no,
                'account_type': matched_account.account_type,
                'balance': matched_account.balance
            }
        }), 200

    # Fallback in case it's a form-based POST (optional)
    return render_template('success.html', message="Only JSON requests supported for withdrawal.")




#check_balance
@app.route('/check_balance', methods=['GET', 'POST'])
def check_balance_route():
    if request.method == 'POST':
        email = request.form.get('email')
        account_number = request.form.get('account_number')

        matched_account = None

        if email:
            for acc in accounts.values():
                if acc.email == email:
                    matched_account = acc
                    break
        if not matched_account and account_number:
            matched_account = accounts.get(account_number)

        if matched_account:
            return render_template(
                'success.html',
                message="Balance fetched successfully.",
                data=matched_account
            )
        else:
            return render_template(
                'success.html',
                message="Account not found."
            )

    return render_template('check_balance.html')

@app.route('/fetch_details', methods=['POST'])
def fetch_details():
    email = request.json.get('email')
    account_number = request.json.get('account_number')

    matched_account = None

    if email:
        for acc in accounts.values():
            if acc.email == email:
                matched_account = acc
                break

    if not matched_account and account_number:
        for acc in accounts.values():
            if acc.account_no == account_number:
                matched_account = acc
                break

    if matched_account:
        return jsonify({
    'status': 'success',
    'data': {
        'first_name': matched_account.first_name,
        'last_name': matched_account.last_name,
        'email': matched_account.email,
        'account_no': matched_account.account_no,
        'account_type': matched_account.account_type,
        'balance': matched_account.balance  
    }
})

if __name__ == '__main__':
    db.fetch_all_accounts_with_users()
    app.run(debug=True)
