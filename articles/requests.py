from models.article import Article

import sqlite3
import json


def get_single_article(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.title,
            a.content,
            a.date,
            a.user_id,
            a.category_id
        FROM articles a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        article = Article(data['id'],data['title'],data['content'], data['date'], data['user_id'], data['category_id'])

        return json.dumps(article.__dict__)

def delete_article(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM articles
        WHERE id = ?
        """, (id, ))
        
def create_article(new_article):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO articles
            ( title, content, date, user_id, category_id)
        VALUES 
            (?, ?, ?, ?, ?);
        """, (new_article['title'], new_article['content'], new_article['date'], new_article['user_id'], new_article['category_id'], ))
        id = db_cursor.lastrowid
        new_article['id'] = id
    return json.dumps(new_article)

def update_article(id, new_article):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE articles
            SET
                title = ?,
                content = ?,
                date = ?,
                user_id= ?,
                category_id= ?
        WHERE id = ?
        """, (new_article['title'], new_article['content'],
              new_article['date'], new_article['user_id'],
              new_article['category_id'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
