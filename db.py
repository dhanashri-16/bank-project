import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dhana",
        database="bank"
    )

def insert_users(first_name, last_name, email):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
    cursor.execute(sql, (first_name, last_name, email))
    conn.commit()
    conn.close()

def insert_accounts(user_id, account_number, account_type, balance=0):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO accounts (user_id, account_number, account_type, balance) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, account_number, account_type, balance))
    conn.commit()
    conn.close()

def fetch_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def fetch_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def fetch_all_accounts_with_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
    SELECT u.user_id, u.first_name, u.last_name, a.account_number, a.account_type, a.balance
    FROM users u
    JOIN accounts a ON u.user_id = a.user_id
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

def get_last_user_id():
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(user_id, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE accounts SET balance = %s WHERE user_id = %s"
    cursor.execute(sql, (new_balance, user_id))
    conn.commit()
    conn.close()

def delete_user_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()

def delete_account(account_number):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM accounts WHERE account_number = %s"
    cursor.execute(sql, (account_number,))
    conn.commit()
    conn.close()

def get_balance_by_account_number(account_number):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT balance FROM accounts WHERE account_number = %s"
    cursor.execute(sql, (account_number,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


