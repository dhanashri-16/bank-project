from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/deposit', methods=['GET', 'POST'])
def deposit_route():
    if request.method == 'POST':
        account_no = request.form['account_no']
        email = request.form['email']
        amount = int(request.form['amount'])  

        account_data = accounts.get(account_no)

        if account_data and account_data.email == email:
            if amount > 0:
                account_data.balance += amount  
                return render_template(
                    'success.html',
                    message=f"Deposit of ₹{amount} successful. New balance: ₹{account_data.balance}",
                    data=account_data
                )
            else:
                return render_template(
                    'success.html',
                    message="Invalid deposit amount.",
                    data=account_data
                )
        else:
            return render_template('success.html', message="Account not found.")
    
    return render_template('deposit.html')



@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw_route():
    if request.method == 'POST':
        account_no = request.form['account_no']
        email = request.form['email']
        amount = int(request.form['amount'])  

        account_data = accounts.get(account_no)

        if account_data and account_data.email == email:
            if amount > 0 and account_data.balance >= amount:
                account_data.balance -= amount  
                return render_template(
                    'success.html',
                    message=f"Withdrawal of ₹{amount} successful. Remaining balance: ₹{account_data.balance}",
                    data=account_data
                )
            else:
                return render_template(
                    'success.html',
                    message="Insufficient balance or invalid amount.",
                    data=account_data
                )
        else:
            return render_template('success.html', message="Account not found.")
    
    return render_template('withdraw.html')


@app.route('/check_balance', methods=['GET', 'POST'])
def check_balance_route():
    if request.method == 'POST':
        account_no = request.form['account_no']
        email = request.form['email']

        account_data = accounts.get(account_no)

        if account_data and account_data.email == email:  
            return render_template(
                'success.html',
                message="Balance fetched successfully.",
                data=account_data
            )
        else:
            return render_template('success.html', message="Account not found.")
    
    return render_template('check_balance.html')



if __name__ == '__main__':
    db.fetch_all_accounts_with_users()
    app.run(debug=True)
