from controllers.controllers import ControllerView
from controllers.catalogcontroller import *
from controllers.userscontroller import *
from utils import *

class BookItemMemberCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            # (self.render_list, "List"),
            # (self.render_add, "Add"),
            # (self.render_edit, "Edit"),
            (self.render_list, "All Availible Bookitems"),
            (self.render_search, "Search Availible Bookitems"),
            (self.render_loan, "Loan a Book"),
            (self.render_loan_list, "Loaned Books"),
            (self.render_return_loan, "Return loaned Books"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]
        self.catalogcv = CatalogAdminCV(CatalogMemberCV)
        self.usercv = MembersCV(ControllerView)
        self.user = self.breadcrumbs[0].user

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_menu(self):
        self.line()
        print("Library management options:")
        ControllerView.render_menu(self)

    def render_loan(self):
        self.line()
        self.render_available_bookitems()
        bookitemid = self.select_field_id('Enter number from column #: ')
        bookitem = self.catalog.getBookItem(bookitemid)
        if bookitem:
            print(f'Book selected: {bookitem.title}')
            if self.loanmanager.loanItemToMember(self.user, bookitem):
                print(f'Book: {bookitem.title} loaned to Member {self.user.id}.{self.user.username}')
        else:
            print(f"Bookitem not found")
    
    def render_loan_list(self):
        self.line()
        print('Loaned bookitems in Library.')
        print(f'{s("#", 3)} - {s("Member")} - {s("Title")} - {s("Author")} - {s("ISBN")} - {s("Issue date")} - {s("Return date")} - {s("Status")}')
        allLoanedItems = self.loanmanager.getLoanItemsByUserId(self.user.id)
        if len(allLoanedItems) == 0:
            print('Empty list.')
        for i,item in enumerate(allLoanedItems):
            print(f'{s(i, 3)} - {s(item.username)} - {s(item.title)} - {s(item.author)} - {s(item.ISBN)} - {s(item.issueDate)} - {s(item.returnDate)} - {s(item.itemStatus)}')

    def render_return_loan(self):
        self.render_loan_list()
        idsstr = str(input('Enter LoanItemID\'s (separated with a space)? '))
        idslist = idsstr.split(' ')
        ids = []
        for id in idslist:
            if id.isdigit():
                ids.append(int(id))
        self.loanmanager.setLoanedItemsReceivedById(ids)
        self.render_loan_list()
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author: '))
        res = self.catalog.searchBookItem(query)
        self.render_list(res)

    def render_list(self, bookitems = None):
        self.line()
        print('Bookitems in Library.')
        # bookitems = self.catalog.listAllBookItems()
        print(f'{s("#", 3)} - {s("Title")} - {s("Author")} - {s("ISBN")} - {s("Status")}')
        if not bookitems:
            bookitems = self.catalog.listAllBookItems()
        if len(bookitems) == 0:
            print('Empty list.')
        for i,item in enumerate(bookitems):
            print(f"{s(i, 3)} - {s(item.title)} - {s(item.author)} - {s(item.ISBN)} - {s(item.itemStatus)}")

    def render_available_bookitems(self):
        self.line()
        print('Available bookitems in Library.')
        print(f'{s("#", 3)} - {s("Title")} - {s("Author")} - {s("ISBN")} - {s("Status")}')
        allLoanedItems = self.loanmanager.getBookItemsAvailable()
        if len(allLoanedItems) == 0:
            print('No booksitem available.')
        for i,item in enumerate(allLoanedItems):
            print(f'{s(i, 3)} - {s(item.title)} - {s(item.author)} - {s(item.ISBN)} - {s(item.itemStatus)}')

class BookItemAdminCV(BookItemMemberCV):
    def __init__(self, *args):
        not self.initialized if BookItemMemberCV.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "All Availible Bookitems"),
            (self.render_search, "Search Availible Bookitems"),
            (self.render_add, "Add Bookitem"),
            (self.render_edit, "Edit Bookitem"),
            (self.render_delete, "Delete Bookitem"),
            (self.render_loan, "Loan a Book to Member"),
            (self.render_loan_list, "Loaned Books"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]
        self.catalogcv = CatalogAdminCV(ControllerView)

    def render_add(self):
        self.line()
        self.catalogcv.render_list()        
        id = None
        book = None
        nbooks = None
        try:
            id = int(input("Enter bookid from column # "))
        except:
            print("Invalid option entered. Retry.")
            self.render_add()
        
        if id >=0:
            book = self.catalog.getBookById(id)
        if book:
            print(f'Book selected {book.id} {book.title}')
            try:
                nbooks = int(input("how many books would you like to add? (default = 1) "))
            except:
                print("Invalid option entered. Retry.")
                self.render_add()
            if nbooks is None:
                nbooks = 1
            for x in range(nbooks):
                bookitem = self.catalog.addBookItem(book)
                print(f'Bookitem {bookitem.title} added')
            self.catalog.listAllBookItems()
        else:
            print('Book not found')
    

    def render_edit(self):
        self.render_list()
        id = None
        bookitem = None
        try:
            id = int(input("Enter bookitem from column #: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()
        if id >=0:
            bookitem = self.catalog.getBookItem(id)
        if bookitem:
            confirm, bookitem = self.edit_form(bookitem)
            if confirm:
                self.catalog.updateBookitem(id, bookitem)
                print(f"Bookitem {bookitem.title} was changed succesfully")
            else:
                print('Bookitem not found. You\'ll now redirected to Library menu.')
        else:
            print('Bookitem not found. You\'ll now redirected to Library menu.')

    def render_delete(self):
        self.line()
        self.render_list()
        id = None
        bookitem = None
        try:
            id = int(input("Enter number from column #: "))
        except:
            print("Invalid number entered. Retry.")
            self.render_delete()
        if id >=0:
            bookitem = self.catalog.getBookItem(id)
        if bookitem:
            is_confirm = input("Confirm delete (input:y) or cancel (press:Enter)? ")
            if is_confirm == 'y':
                if self.catalog.deleteBookitem(id):
                    print(f"Bookitem {bookitem.title} was deleted succesfully")
                else:
                    print(f"Bookitem {bookitem.title} was NOT deleted")
            else:
                print(f"Bookitem {bookitem.title} was NOT deleted")
        else:
            print('Bookitem not found. You\'ll now redirected to Library menu.')

    def render_loan_list(self):
        self.line()
        print('Loaned bookitems in Library.')
        print(f'{s("#", 3)} - {s("Member")} - {s("Title")} - {s("Author")} - {s("ISBN")} - {s("Issue date")} - {s("Return date")} - {s("Status")}')
        allLoanedItems = self.loanmanager.listAllBookItemsLoaned()
        if len(allLoanedItems) == 0:
            print('Empty list.')
        for i,item in enumerate(allLoanedItems):
            print(f'{s(i, 3)} - {s(item.username)} - {s(item.title)} - {s(item.author)} - {s(item.ISBN)} - {s(item.issueDate)} - {s(item.returnDate)} - {s(item.itemStatus)}')


    def render_loan(self):
        self.line()
        self.render_available_bookitems()
        print("Loan a Bookitem to a Member")
        bookitemid = self.select_field_id('Enter number from column #: ')
        bookitem = self.catalog.getBookItem(bookitemid)
        if bookitem:
            print(f'Book selected: {bookitem.title}')
            self.usercv.render_list()
            userid = self.select_field_id('Enter number from column #: ')
            user = self.usermanager.findbyid(userid)
            if user:
                print(f'User selected: {user.username}')
                if self.loanmanager.loanItemToMember(user, bookitem):
                    print(f'Book: {bookitem.title} loaned to Member {userid}.{user.username}')
            else:
                print(f"User not found")
        else:
            print(f"Bookitem not found. You\'ll now redirected to Library menu")

