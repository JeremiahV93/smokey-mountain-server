from models.user import User

import sqlite3
import json

def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.display_name,
            u.date
        FROM users u
        WHERE u.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'],data['first_name'],data['last_name'], data['email'], data['display_name'], data['date'])

        return json.dumps(user.__dict__)



def create_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO users
            ( first_name, last_name, email, display_name, date)
        VALUES 
            (?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['display_name'], new_user['date'], ))
        id = db_cursor.lastrowid
        new_user['id'] = id
    return json.dumps(new_user)
