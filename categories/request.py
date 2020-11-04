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
