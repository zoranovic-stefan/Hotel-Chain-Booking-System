from flask_login import UserMixin

class LoginUser(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def get_id(self):
        return f"{self.role}:{self.id}"