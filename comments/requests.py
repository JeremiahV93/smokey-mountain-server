from models.comment import Comment
from models.user import User, Usercomment

import sqlite3
import json

def get_all_comments_by_article(article_id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.article_id,
            c.content,
            c.user_id,
            c.date,
            c.subject,
            u.display_name
        FROM comments c
        JOIN users u 
            ON u.id = c.user_id
        WHERE c.article_id = ?
        """, (article_id, ))

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['article_id'], row['content'], row['user_id'], row['date'], row['subject'])
            user = Usercomment(row['user_id'], row['display_name'])
            comment.user = user.__dict__
            comments.append(comment.__dict__)

        return json.dumps(comments)

def create_comment(new_comment):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            ( article_id, content, user_id, date, subject )
        VALUES
            (?, ?, ?, ?, ?);
        """, (new_comment['article_id'], new_comment['content'], new_comment['user_id'], new_comment['date'], new_comment['subject'], ))
        id = db_cursor.lastrowid
        new_comment['id'] = id
    return json.dumps(new_comment)
    
def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))

def update_comment(id, new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE comments
            SET
                article_id = ?,
                content = ?,
                user_id = ?,
                date = ?,
                subject = ?
        WHERE id = ?
        """, (new_comment['article_id'], new_comment['content'], new_comment['user_id'], new_comment['date'], new_comment['subject'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True
