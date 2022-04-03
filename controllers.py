from models import *
from usermodels import *

class ControllerView:
    def __init__(self, *args):
        self.user = False
        self.login_form()
        # self.navigation_options()

    def login_form(self):
        inp_username = str(input('Username:'))
        inp_password = str(input('Password:'))

        _user = Person.findbyname(inp_username)
        if (_user and inp_username == _user.username and inp_password == _user.password):
            self.user = _user
            print('Welcome,{username}!'.format(username = _user.username))
        else:
            print('Password or Username is incorrect')
        return self.user
    # def navigation_options(self):
    #     menu_options = (
    #         {""}
    #     )
        
    #     print()
    # def add_user_form(self):
    #     print("abc")
