from models.comment import Comment

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
            c.subject
        FROM comments c
        WHERE c.article_id = ?
        """, (article_id, ))

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['article_id'], row['content'], row['user_id'], row['date'], row['subject'])

            comments.append(comment.__dict__)

        return json.dumps(comments)
