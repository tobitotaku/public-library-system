from models import *
from usermodels import *

class ControllerView:
    def __init__(self, *args):
        self.user = False
        self.menu_item = {}
        self.menu_option_list = {}
        self.menu_action_list = {}
    
    def set_menu_options_actions(self):
        i = 0
        for item in self.menu_item:
            i += 1
            # print(type(item))
            self.menu_action_list[i] = item
            self.menu_option_list[i] = self.menu_item[item]

    def render_menu(self):
        inp_option = False
        self.set_menu_options_actions()
        # _options.key should match _actions.key
        for item in self.menu_option_list:
            txt = "{number}. {label}".format(number = item, label = self.menu_option_list[item])
            print(txt)
        
        while True:
            try:
                inp_option = int(input("Enter a menu option:"))
                break
            except:
                print("invalid menu option. input should be integer")
                
        if (inp_option and inp_option in self.menu_action_list):
            # try:
            _method = getattr(self, self.menu_action_list[inp_option])
            _method()
            # except:
            #     print("Error: action not found")
        else:
            print("entered number is not a menu options")

        return inp_option

class UsersCV(ControllerView):
    def __init__(self, *args):
        ControllerView.__init__(self, *args)
        # self.user = False
        self.render_login()
        self.menu_item = {
            "render_add_member":"Add a member",
            "render_edit_member":"Edit a member",
            "render_list_member":"List all members",
            "render_delete_member":"Delete a member",
        }
        self.render_menu()

    def render_login(self):
        inp_username = str(input('Username:'))
        inp_password = str(input('Password:'))

        user = Person.findbyname(inp_username)
        if (user and inp_username == user.username and inp_password == user.password):
            self.user = user
            print('Welcome,{username}!'.format(username = user.username))
        else:
            print('Password or Username is incorrect')
        return self.user

    def render_menu(self):
        print("Menu Options:")
        ControllerView.render_menu(self)

    def render_add_member(self):
        print("Enter member in field:")
        username = input("1. username> ")
        # input("confirm? yes[y]/no[n]")

        user = Person.findbyname(username)
        if user:
            print('Member: {name} already exists'.format(name = user.username))
        else:
            surname = input("2. surname> ")
            age = input("3. age> ")
            password = input("4. password> ")
            new_member = Member(
                username,
                surname,
                age,
                password
            )
            new_member.add()
            print("Member {username} was added succesfully".format(username = username))
    def render_list_member(self):
        print('list of active members')
        print('- # - username - surname - age -')
        list = Person.allmembers()
        i = 0
        for item in list:
            user = item
            i+= 1
            print('- {i} - {name} - {surname} - {age} -'.format(i = i, name = user.username, surname = user.surname, age = user.age ))
        return list
    def render_edit_member(self):
        list = self.render_list_member()
        username = str(input("to edit, type username of member> "))
        user = Person.findbyname(username, list)
        if user:
            surname = input("2. surname> ")
            age = input("3. age> ")
            password = input("4. password> ")
            user = Member(
                username,
                surname,
                age,
                password
            )
            user.update()
        else:
            print('Member not found')


