
import sqlite3

class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        except:
            cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
            raise UserNotFoundError('The table `users` did not exist, but it was created. Run the registration again.')
        finally:
            connection.commit()
            connection.close()
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        try:
            data = cursor.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            if data:
                return cls(data[1], data[2])
        finally:
            connection.close()