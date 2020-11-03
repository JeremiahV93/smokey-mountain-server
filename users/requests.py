from models.user import User

import sqlite3
import json

def get_single_user():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.diplay_name,
            u.date
        FROM users u
        WHERE u.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'],data['first_name'],data['last_name'], data['email'], data['display_name'], data['date'])

        return json.dumps(user.__dict__)
