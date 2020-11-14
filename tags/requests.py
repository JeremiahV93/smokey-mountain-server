from models.tag import Tag

import sqlite3
import json 

def get_all_tags():
    with sqlite3.connect('./rare/db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.title
        FROM tags u
        """)

def get_single_tag(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.title
        FROM tags u
        WHERE u.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'],data['title'])

        return json.dumps(tag.__dict__)



def create_tag(new_tag):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO tags
            ( title )
        VALUES 
            (?, ?, ?, ?, ?);
        """, (new_tag['title'], ))
        id = db_cursor.lastrowid
        new_tag['id'] = id
    return json.dumps(new_tag)

def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM tags
        WHERE id = ?
        """, (id, ))

def update_tag(id, new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE tags
            SET
                title =?
        WHERE id = ?
        """, (new_tag['title'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True
