from controllers import *

class MembersCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        # self.user = False
        # self.render_login()
        # self.render_edit()
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            (self.render_edit, "Edit"),
            (self.render_delete, "Delete"),
            (exit, "Exit application"),
        ]
        self.render_menu() # for tests only

    def render_menu(self):
        print("Members management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        print("Enter member in fields:")
        username = input("1. username? ")
        # input("confirm? yes[y]/no[n]")

        user = self.usermanager.findbyname(username)
        if user:
            print('Member: {username} already exists'.format(**user.__dict__))
            is_continue = str(input('Would like to a another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_add()
        else:
            user = self.usermanager.add(
                username,
                input("2. surname? "),
                input("3. age? "),
                input("4. password? ")
            )
            print("Member {username} was added succesfully".format(**user.__dict__))
        
        self.render_menu()

    def render_list(self):
        print('list of active members')
        print('- ID - username - surname - age -')
        list = self.usermanager.users
        for item in list:
            print('- {id} - {username} - {surname} - {age} -'.format(**item.__dict__))
        return list

    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Select & Edit member by typing their ID: "))
        except:
            print("Invalid option entered. Enter an ID")
            self.render_edit()

        user = self.usermanager.findbyid(id)
        if user:
            user.username = input("1. username? ")
            user.surname = input("2. surname? ")
            user.age = input("3. age? ")
            user.password = input("4. password? ")
            self.usermanager.update(id, user)
            print("Member {username} was changed succesfully".format(**user.__dict__))
        else:
            print('Member not found')
            is_continue = str(input('Would like to edit another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_edit()

        self.render_menu()

    def render_delete(self):
        self.render_list()
        try:
            id = int(input("Select & Delete member by typing their ID: "))
        except:
            print("Invalid ID entered. Enter an ID")
            self.render_delete()
        user = self.usermanager.findbyid(id)
        if user:
            is_confirm = input("confirm delete? [confirm with: y (for yes) or press Enter]")
            if is_confirm == 'y':
                self.usermanager.delete(id)
                print("Member {username} was deleted succesfully".format(**user.__dict__))
            else:
                print("Member {username} was NOT deleted".format(**user.__dict__))
        else:
            print('Member not found')
            is_continue = str(input('Would like to Delete another Member? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_delete()

        self.render_menu()

# cv = MembersCV() # for testing
