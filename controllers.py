from models import *
from userManager import *

class ControllerView:
    def __init__(self, *args):
        self.user = False
        self.actions = []
        self.stop = False

    def render_menu(self): 
        if self.stop:
            return 0

        inp_option = False
        # _options.key should match _actions.key
        i = 0
        for item in self.actions:
            print("{i}. {1}".format(i = i,*item))
            i += 1
        try:
            inp_option = int(input("Enter a menu option:"))
            callback = self.actions[inp_option][0]
        except:
            print("Invalid menu option. Enter the ID of the menu option")
            self.render_menu()
        
        callback()
        self.render_menu()
        return inp_option

class UsersCV(ControllerView):
    def __init__(self, *args):
        ControllerView.__init__(self, *args)
        # self.user = False
        # self.render_login()
        self.actions = [
            (self.render_list_member, "List all members"),
            (self.render_add_member, "Add a member"),
            (self.render_edit_member, "Edit a member"),
            (self.render_delete_member, "Delete a member"),
        ]
        self.render_menu()

    def render_login(self):
        inp_username = str(input('Username:'))
        inp_password = str(input('Password:'))

        user = UserManager.findbyname(inp_username)
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

        user = UserManager.findbyname(username)
        if user:
            print('Member: {username} already exists'.format(**user.__dict__))
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
            print("Member {username} was added succesfully".format(**user.__dict__))

    def render_list_member(self):
        print('list of active members')
        print('- # - username - surname - age -')
        list = UserManager().users
        i = 0
        for item in list:
            print('- {i} - {username} - {surname} - {age} -'.format(i = i, **item.__dict__))
            i+= 1
        return list

    def render_edit_member(self):
        list = self.render_list_member()
        username = str(input("Select member to edit by typing username> "))
        user = UserManager.findbyname(username, list)
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

    def render_delete_member():
        pass


