from controllers import * 
from controllers import ControllerView

class MembersCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            (self.render_edit, "Edit"),
            (self.render_delete, "Delete"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')
 
    def render_menu(self):
        self.line()
        print("Members management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        self.line()
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
        self.line()
        print('list of active members')
        print('- ID - username - surname - age -')
        if len(self.usermanager.users) == 0:
            print('Empty list.')
        for item in self.usermanager.users:
            print('- {id} - {username} - {surname} - {age} -'.format(**item.__dict__))

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
        self.line()
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

# MembersCV().render_menu() # for testing
