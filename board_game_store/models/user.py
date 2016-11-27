from flask_login import UserMixin

class User(UserMixin):

    is_authenticated = False
    name = "PLACEHOLDER"

    def __init__(self, cpf):
        self.cpf = cpf

    def is_authenticated():
        # TODO
        return self.is_authenticated

    def get_id():
        return self.cpf

    def get_id(user):
        return user.cpf

    def is_active():
        return True

    def is_anonymous():
        return False
