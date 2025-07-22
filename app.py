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
        new_account = BankAccount(first, last, acc_type, balance)
        accounts[new_account.account_no] = new_account
        db.insert_users(first, last, email)
        db.insert_accounts(new_account.user_id, new_account.account_no, new_account.account_type, new_account.balance)
        return render_template('success.html', message="Account created successfully!", data=new_account)
    return render_template('create_account.html')
#deposit
@app.route('/deposit', methods=['GET', 'POST'])
def deposit_route():
    if request.method == 'POST':
        email = request.form.get('email')
        account_number = request.form.get('account_number')
        amount = request.form.get('amount')

        if not all([email, account_number, amount]):
            return render_template('success.html', message="Missing details.")

        matched_account = None

        
        for acc in accounts.values():
            if acc.email == email:
                matched_account = acc
                break

        if not matched_account or matched_account.account_no != account_number:
            return render_template('success.html', message="Account not found or mismatch.")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return render_template('success.html', message="Invalid deposit amount.")

        matched_account.balance += amount


        db.update_balance(matched_account.account_no, matched_account.balance)

        return render_template(
            'success.html',
            message=f"Deposit of ₹{amount} successful. New balance: ₹{matched_account.balance}",
            data=matched_account
        )
    return render_template('deposit.html')


@app.route('/deposit', methods=['POST'])
def deposit():
    email = request.json.get('email')
    account_number = request.json.get('account_number')
    amount = request.json.get('amount')

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
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid deposit amount.'}), 400

    matched_account.balance += amount

    db.update_balance(matched_account.account_no, matched_account.balance)

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

#withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw_route():
    if request.method == 'POST':
        email = request.form.get('email')
        account_number = request.form.get('account_number')
        amount = request.form.get('amount')

        if not all([email, account_number, amount]):
            return render_template('success.html', message="Missing details.")

        matched_account = None

        for acc in accounts.values():
            if acc.email == email:
                matched_account = acc
                break

        if not matched_account or matched_account.account_no != account_number:
            return render_template('success.html', message="Account not found or mismatch.")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return render_template('success.html', message="Invalid withdrawal amount.")

        if matched_account.balance < amount:
            return render_template('success.html', message="Insufficient balance.")

        matched_account.balance -= amount

        return render_template(
            'success.html',
            message=f"Withdrawal of ₹{amount} successful. New balance: ₹{matched_account.balance}",
            data=matched_account
        )

    return render_template('withdraw.html') 

@app.route('/withdraw', methods=['POST'])
def withdraw():
    email = request.json.get('email')
    account_number = request.json.get('account_number')
    amount = request.json.get('amount')

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
        return jsonify({
            'status': 'error',
            'message': 'Account not found.'
        }), 404

    if matched_account.account_no != account_number:
        return jsonify({
            'status': 'error',
            'message': 'Email and account number do not match.'
        }), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid withdrawal amount.'
        }), 400

    if matched_account.balance < amount:
        return jsonify({
            'status': 'error',
            'message': 'Insufficient balance.'
        }), 400

    matched_account.balance -= amount

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
