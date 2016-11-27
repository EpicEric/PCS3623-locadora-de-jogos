from board_game_store.db.access import get_employee_name_by_cpf
from flask_login import UserMixin

class User(UserMixin):

    usernames = {}
    is_authenticated = False
    name = "PLACEHOLDER"

    def __init__(self, cpf):
        self.cpf = cpf
        if (cpf not in self.usernames):
            name_tuple = get_employee_name_by_cpf(cpf)
            self.usernames[cpf] = name_tuple[0] + " " + name_tuple[1]
        self.name = self.usernames[cpf]
        print(self.usernames)

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
