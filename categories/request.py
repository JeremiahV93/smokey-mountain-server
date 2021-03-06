from models.category import Category

import sqlite3
import json

def get_all_categories():
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.title
        FROM categories c
        """)

        categories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['title'])

            categories.append(category.__dict__)

    return json.dumps(categories)

def get_category_by_id(id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.title
        FROM categories c
        WHERE c.id = ?
        """, (id, ))

        data = db_cursor.fetchone()
        
        category = Category(data['id'], data['title'])

        return json.dumps(category.__dict__)

def delete_category(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
        """, (id, ))

def update_category(id, update_obj):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE categories
            Set
                title = ?
        WHERE id =?
        """, (update_obj['title'], id ))

        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def create_category(new_obj):
     with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO categories
            (title)
        VALUES (?)
        """, (new_obj['title'],  ))

        id =  db_cursor.lastrowid

        new_obj['id'] = id
        return json.dumps(new_obj)
