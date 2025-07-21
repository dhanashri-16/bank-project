import random
import db

class BankAccount:
    def __init__(self, first_name, last_name, account_type, initial_balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_type = account_type
        self.balance = initial_balance
        self.user_id = self._generate_user_id()
        self.account_no = self._generate_account_no()  # Moved here properly

    

    def _generate_account_no(self):
        fixed_part = "12345"
        random_part = str(random.randint(10000, 99999))
        return fixed_part + random_part

    def _generate_user_id(self):
        last_user_id = db.get_last_user_id()
        print(last_user_id)
        return last_user_id + 1

    def deposit(self, amount):
        self.balance += amount
        db.update_balance(self.user_id, self.balance)
        print(f"Deposit successful. New balance: ₹{self.balance:.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            db.update_balance(self.user_id, self.balance)
            print(f"Withdrawal successful. New balance: ₹{self.balance:.2f}")
            return True

    def display_account_info(self):
        print(f"Account No: {self.account_no}, Name: {self.first_name} {self.last_name}, "
              f"Type: {self.account_type}, Balance: ₹{self.balance:.2f}, User ID: {self.user_id}")

 
# Global dictionary to store accounts
accounts = {}

def load_existing_accounts():
    existing_accounts = db.fetch_all_accounts_with_users()
    for acc in existing_accounts:
        acc_obj = BankAccount(
            acc['first_name'],
            acc['last_name'],
            acc['account_type'],
            acc['balance']
        )
        acc_obj.account_no = acc['account_number']
        acc_obj.user_id = acc['user_id']
        accounts[acc_obj.account_no] = acc_obj


def create_account():
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    email = input("Enter your email: ")
    acc_type = input("Enter account type (Savings/Current): ")
    balance = float(input("Enter initial balance: "))
    new_account = BankAccount(first, last, acc_type, balance)
    accounts[new_account.account_no] = new_account
    print("Account created successfully!")
    db.insert_users(first, last, email)
    db.insert_accounts(new_account.user_id, new_account.account_no, new_account.account_type, new_account.balance)
    new_account.display_account_info()


def deposit_to_account():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        amount = float(input("Enter amount to deposit: "))
        accounts[acc_no].deposit(amount)
    else:
        print("Account not found.")


def withdraw_from_account():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        amount = float(input("Enter amount to withdraw: "))
        accounts[acc_no].withdraw(amount)
    else:
        print("Account not found.")


def check_balance():
    acc_no = input("Enter account number to check balance: ")
    if acc_no in accounts:
        print(f"Current balance: ₹{accounts[acc_no].balance:.2f}")
    else:
        print("Account not found.")


def delete_user():
    user_id = int(input("Enter user ID to delete: "))
    found = False
    for acc_no, acc in list(accounts.items()):
        if acc.user_id == user_id:
            del accounts[acc_no]
            db.delete_user_by_user_id(user_id)
            db.delete_account(acc_no)
            print("User and associated account deleted successfully.")
            found = True
            break
    if not found:
        print("User ID not found.")


# Load accounts from database before starting
load_existing_accounts()

# Main Menu
#while True:
    #print("1. Create Account")
    #print("2. Deposit")
    #print("3. Withdraw")
    #print("4. Check Balance")
    #print("5. Delete User")
    #print("6. Exit")
    #choice = input("Enter your choice: ")

    #if choice == '1':
        #create_account()
    #elif choice == '2':
        #deposit_to_account()
    #elif choice == '3':
        #withdraw_from_account()
    #elif choice == '4':
        #check_balance()
    #elif choice == '5':
        #delete_user()
    #elif choice == '6':
        #print("Thank you for using the banking system.")
        #break
    #else:
        #print("Invalid choice. Please try again.")






