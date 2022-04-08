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
        # self.render_edit_member()
        self.actions = [
            (self.render_list_member, "List all members"),
            (self.render_add_member, "Add a member"),
            (self.render_edit_member, "Edit a member"),
            (self.render_delete_member, "Delete a member"),
            (exit, "Exit application"),
        ]
        self.render_menu()

    def render_login(self):
        inp_username = str(input('Username:'))
        inp_password = str(input('Password:'))

        user = UserManager().findbyname(inp_username)
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
        print("Enter member in fields:")
        username = input("1. username? ")
        # input("confirm? yes[y]/no[n]")

        user = UserManager().findbyname(username)
        if user:
            print('Member: {username} already exists'.format(**user.__dict__))
            is_continue = str(input('Would like to a another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_add_member()
        else:
            new_member = Person(
                username,
                input("2. surname? "),
                input("3. age? "),
                input("4. password? ")
            )
            user = UserManager().add(new_member)
            print("Member {username} was added succesfully".format(**user.__dict__))
        
        self.render_menu()

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
        username = str(input("Select & Edit member by typing their username: "))
        user = UserManager().findbyname(username)
        if user:
            user = Person(
                username,
                input("2. surname? "),
                input("3. age? "),
                input("4. password? ")
            )
            UserManager().update(username, user)
            print("Member {username} was changed succesfully".format(**user.__dict__))
        else:
            print('Member not found')
            is_continue = str(input('Would like to edit another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_edit_member()

        self.render_menu()

    def render_delete_member(self):
        username = str(input("Select & Delete member by typing their username: "))
        user = UserManager().findbyname(username)
        if user:
            is_confirm = input("confirm delete? [confirm with: y (for yes) or press Enter]")
            if is_confirm == 'y':
                UserManager().delete(username)
                print("Member {username} was deleted succesfully".format(**user.__dict__))
            else:
                print("Member {username} was NOT deleted".format(**user.__dict__))
        else:
            print('Member not found')
            is_continue = str(input('Would like to Delete another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_delete_member()

        self.render_menu()


