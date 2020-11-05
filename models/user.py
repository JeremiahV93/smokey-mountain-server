class User():
    def __init__(self, id, first_name, last_name, email, display_name, date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.display_name = display_name
        self.date = date

class Usercomment():
    def __init__(self, id, display_name):
        self.id = id
        self.display_name = display_name
