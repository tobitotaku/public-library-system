from controllers.controllers import ControllerView

class LoanItemMemberCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            # (self.render_edit, "Edit"),
            # (self.render_delete, "Delete"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]
    
    def render_add(self):
        pass

    def render_list(self):
        self.line()
        print('list of active members')
        print('- ID - username - surname - age -')
        if len(self.usermanager.users) == 0:
            print('Empty list.')
        for item in self.usermanager.users:
            print(f'- {item.id} - {item.username} - {item.surname} - {item.age} -')

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')
 
    def render_menu(self):
        self.line()
        print("Loan management options:")
        ControllerView.render_menu(self)

class LoanItemAdminCV(LoanItemMemberCV):
    # def __init__(self, *args):
    #     not self.initialized if LoanItemMemberCV.__init__(self, *args) else self.initialized
    #     self.actions = [
    #         (self.render_add, "Add"),
    #         (self.render_edit, "Edit"),
    #         (self.render_delete, "Delete"),
    #         (self.render_import, "Import JSON"),
    #     ] + self.actions

    def render_add(self):
        self.line()
        self.bookitemcv.render_list()
        bookitemid = input("[0] Enter a BookItemID? ")
        # input("confirm? yes[y]/no[n]")

        bookitem = self.catalog.getBookItem(bookitemid)
        if bookitem:
            book = self.catalog.getBookById(bookitem.bookid)
            print(f'Book selected: {bookitem.id} - {book.title}')

            self.usercv.render_list()
            userid = input("[0] Enter a UserID? ")
            user = self.usercv.findbyid(userid)
            if user:
                print(f'User selected: {user.id} - {user.username}')
                self.loanmanager.add(user, bookitem)
            else:
                print(f"User not found")
        else:
            print(f"Bookitem not found")
        

# MembersCV().render_menu() # for testing
