
import sqlite3


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, username, password, group_id, role_id):
        self.username = username
        self.password = password
        self.group_id = group_id
        self.role_id = role_id

    def save_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        try:
            cursor.execute(
                'INSERT INTO users (username, password, group_id, role_id) VALUES (?, ?, ?, ?)',
                (self.username, self.password, self.group_id, self.role_id))
        except:
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, group_id TEXT, role_id TEXT)')
            raise UserNotFoundError(
                'The table `users` did not exist, but it was created. Run the registration again.')
        finally:
            connection.commit()
            connection.close()

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        try:
            data = cursor.execute(
                'SELECT * FROM users WHERE username=?', (username,)).fetchone()
            if data:
                return cls(data[1], data[2], data[3], data[4])
        finally:
            connection.close()
