class Article():
    def __init__(self, id, title, content, date, user_id, category_id):
        self.id = id
        self.title = title
        self.content = content
        self.date = date
        self.user_id = user_id
        self.category_id = category_id
        self.user = None
