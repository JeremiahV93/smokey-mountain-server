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

def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))
