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
