from controllers.controllers import ControllerView

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
            print(f'Member: {user.username} already exists')
        else:
            user = self.usermanager.add(
                username,
                input("2. surname? "),
                input("3. age? "),
                input("4. password? ")
            )
            print(f"Member {user.username} was added succesfully")
        
    def render_list(self):
        self.line()
        print('list of active members')
        print('- ID - username - surname - age -')
        if len(self.usermanager.users) == 0:
            print('Empty list.')
        for item in self.usermanager.users:
            print(f'- {item.id} - {item.username} - {item.surname} - {item.age} -')

    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()

        user = self.usermanager.findbyid(id)
        if user:
            confirm, user = self.edit_form(user)
            if confirm:
                self.usermanager.update(id, user)
                print(f"Member {user.username} was changed succesfully")
        else:
            print('Member not found')

    def render_delete(self):
        self.line()
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid ID entered. Retry.")
            self.render_delete()
        user = self.usermanager.findbyid(id)
        if user:
            is_confirm = input("Confirm delete?  (y/Enter) ")
            if is_confirm == 'y':
                self.usermanager.delete(id)
                print(f"Member {user.username} was deleted succesfully")
            else:
                print(f"Member {user.username} was NOT deleted")
        else:
            print('Member not found')

# MembersCV().render_menu() # for testing
