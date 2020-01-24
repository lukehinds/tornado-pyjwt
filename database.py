import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

ADMIN_ROLE_ID = '1'

def create_account(username, password, group_id, role_id):
    connection =  sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
            """INSERT INTO users ("username", "password", "group_id", "role_id") VALUES (?, ?, ?, ?)""",
            (username, generate_password_hash(password), group_id, role_id)
            )
    connection.commit()
    connection.close()

def verify_user_credentials(username, password):
    print(password)
    connection =  sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:
        data = cursor.execute(
                    'SELECT * FROM users WHERE username=?', (username,)).fetchone()
    finally:
         connection.close()
    print(data[2])
    if data and check_password_hash(data[2], password):
        return data
    else:
        return False
    
def get_account_details(username):
    connection =  sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:
        data = cursor.execute(
                    'SELECT * FROM users WHERE username=?', (username,)).fetchone()
    finally:
         connection.close()
    return data

def delete_account():
    connection =  sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:
        data = cursor.execute(
                    'DELETE * FROM users WHERE username=?', (username,)).fetchone()
    finally:
         connection.close()
    return data