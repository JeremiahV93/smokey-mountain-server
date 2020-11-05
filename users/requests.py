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

def check_user(email):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()    
    
        db_cursor.execute("""
            SELECT
                u.email
            FROM users u
            WHERE u.email = ?
            """, (email, ))
            
        data = db_cursor.fetchone()
        
        if data:
            return True
        else:
            return False
        

def create_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
       
        user_status = check_user(new_user['email'])
        
        if user_status == False:
            db_cursor.execute("""
            INSERT INTO users
                ( first_name, last_name, email, display_name, date)
            VALUES 
                (?, ?, ?, ?, ?);
            """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['display_name'], new_user['date'], ))
            id = db_cursor.lastrowid
            new_user['id'] = id
            return json.dumps(new_user)

def delete_user(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM users
        WHERE id = ?
        """, (id, ))

def update_user(id, new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                display_name = ?,
                date = ?
        WHERE id = ?
        """, (new_user['first_name'], new_user['last_name'],
              new_user['email'], new_user['display_name'],
              new_user['date'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
