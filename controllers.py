from models import *
# from usermodels import *
from userManager import *
class ControllerView:
    def __init__(self, *args):
        self.user = False
        self.render_login()
        self.menu_option_list = {
            1:"Add a member",
        }
        self.menu_action_list = {
            1:"render_add_member",
        }
        self.render_menu_options()

    def render_login(self):
        inp_username = str(input('Username:'))
        inp_password = str(input('Password:'))

        _user = Person.findbyname(inp_username)
        if (_user and inp_username == _user.username and inp_password == _user.password):
            self.user = _user
            print('Welcome,{username}!'.format(username = _user.username))
        else:
            print('Password or Username is incorrect')
        return self.user

    def render_menu_options(self):
        print(
            "Menu Options:"
        )
        inp_option = False
        # _options.key should match _actions.key
        for item in self.menu_option_list:
            txt = "{number}. {label}".format(number = item, label = self.menu_option_list[item])
            print(txt)
        
        try:
            inp_option = int(input("Enter a menu option:"))
        except:
            print("invalid menu option. input should be integer")
            
        if (inp_option and inp_option in self.menu_action_list):
            try:
                _method = getattr(self, self.menu_action_list[inp_option])
                _method()
            except:
                print("Error: action not found")
        else:
            print("entered number is not a menu options")

        return inp_option

    def render_add_member(self):
        print("Enter member in field:")
        resolver = DataResolver()
        username = input("1# username>")
        surname = input("2# surname>")
        age = input("3# age>")
        password = input("4# password>")

        member_record = Member(
            username,
            surname,
            age,
            password
        ),
        # input("confirm? yes[y]/no[n]")

        _user = Person.findbyname(username)
        print(_user)

