from controllers.controllers import ControllerView
from controllers.catalogcontroller import *
from controllers.userscontroller import *

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
        self.render_list()
        bookitemid = self.select_field_id('[0] Selected BookItemID? ')
        bookitem = self.catalog.getBookItem(bookitemid)
        if bookitem:
            book = self.catalog.getBookById(bookitem.bookid)
            print(f'Book selected: {bookitem.id} - {book.title}')
            self.loanmanager.loanItemToMember(self.user, bookitem)
            print(f'Book: {bookitem.id}.{book.title} loaned to Member {self.user.id}.{self.user.username}')
        else:
            print(f"Bookitem not found")
    
    def render_loan_list(self):
        self.line()
        loanlist = self.loanmanager.getCompleteBookItemLoanedByUserId(self.user.id)
        print('Bookitems in Library.')
        print('- ID - bookitemid - member - Title - Author - ISBN - IssueDate - ReturnDate')
        if len(loanlist) == 0:
            print('Empty list.')
        for item in loanlist:
            loanitem = item['item']
            book = item['book']
            person = self.user
            print(f" - {loanitem.id} - {loanitem.bookItemId} - {person.username} {person.surname} - {book.title} - {book.author} - {book.ISBN} - {loanitem.issueDate} - {loanitem.returnDate} - ")

    def render_return_loan(self):
        self.render_loan_list()
        idsstr = str(input('Selected LoanItem IDS? '))
        idslist = idsstr.split(' ')
        ids = []
        for id in idslist:
            if id.isdigit():
                ids.append(int(id))
        self.loanmanager.setLoanedItemsReceivedById(ids)
        self.render_loan_list()
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author, ISBN: '))
        res = self.loanmanager.searchBookItemWithAvailability(query)
        for item in res:
            book = item[0]
            bookitem = item[1]
            print(f" - {bookitem.id} - {book.title} - {book.author} - {book.ISBN} - {item[2]} - ")
    def render_list(self):
        self.line()
        print('Bookitems in Library.')
        bookitems = self.loanmanager.getBookItemWithAvailability()
        print('- ID - bookid - Author - Title - ISBN -')
        if len(bookitems) == 0:
            print('Empty list.')
        for item in bookitems:
            book = item[0]
            bookitem = item[1]
            print(f" - {bookitem.id} - {book.title} - {book.author} - {book.ISBN} - {item[2]} - ")

class BookItemAdminCV(BookItemMemberCV):
    def __init__(self, *args):
        not self.initialized if BookItemMemberCV.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "All Availible Bookitems"),
            (self.render_list, "Search Availible Bookitems"),
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
        try:
            id = int(input("[0] bookid? "))
        except:
            print("Invalid option entered. Retry.")
            self.render_add()
        
        book = self.catalog.getBookById(id)
        if book:
            print(f'Book selected {book.id} {book.title}')
            bookitem = self.catalog.addBookItem(id)
            print(f'Bookitem {bookitem.id} added')
            self.catalog.listAllBookItems()
        else:
            print('Book not found')
    

    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()

        bookitem = self.catalog.getBookItem(id)
        if bookitem:
            # confirm, book = self.edit_form(book)
            book = self.catalog.getBookById(bookitem.bookid)
            confirm_field = input(f"[{bookitem.id}] Book: [{book.title}] | edit field or skip? (y/Enter) ")
            if confirm_field == 'y':
                print('Books in Catalog')
                self.catalogcv.render_list()
                try:
                    bookid = int(input(f'[0] Bookid? '))
                except:
                    print("Invalid ID entered. Retry.")
                    self.render_edit()
                confirm_save = input('Save changes or skip? (y/Enter) ')
                if confirm_save == 'y':
                    bookitem.bookid = bookid
                    self.catalog.updateBookitem(id, bookitem)
                    print(f"Bookitem {bookitem.id} was changed succesfully")
        else:
            print('Bookitem not found')

    def render_delete(self):
        self.line()
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid ID entered. Retry.")
            self.render_delete()
        bookitem = self.catalog.getBookItem(id)
        if bookitem:
            is_confirm = input("Confirm delete?  (y/Enter) ")
            if is_confirm == 'y':
                self.catalog.deleteBookitem(id)
                print(f"Bookitem {bookitem.id} was deleted succesfully")
            else:
                print(f"Bookitem {bookitem.id} was NOT deleted")
        else:
            print('Bookitem not found')

    def render_loan_list(self):
        self.line()
        print('Bookitems in Library.')
        print('- ID - member - Title - Author - ISBN - IssueDate - ReturnDate')
        allLoanedItems = self.loanmanager.listAllBookItemsLoaned()
        if len(allLoanedItems) == 0:
            print('Empty list.')
        for item in allLoanedItems:
            loanitem = item['item']
            # bookitem = item[1]
            book = item['book']
            person = item['user']
            print(f" - {loanitem.id} - {person.username} {person.surname} - {book.title} - {book.author} - {book.ISBN} - {loanitem.issueDate} - {loanitem.returnDate} - ")

    def render_loan(self):
        self.line()
        self.render_list()
        bookitemid = self.select_field_id('[0] Selected BookItemID? ')
        bookitem = self.catalog.getBookItem(bookitemid)
        if bookitem:
            book = self.catalog.getBookById(bookitem.bookid)
            print(f'Book selected: {bookitem.id} - {book.title}')
            self.usercv.render_list()
            userid = self.select_field_id('[1] Selected UserID? ')
            user = self.usermanager.findbyid(userid)
            if user:
                print(f'User selected: {user.id} - {user.username}')
                self.loanmanager.loanItemToMember(user, bookitem)
                print(f'Book: {bookitem.id}.{book.title} loaned to Member {userid}.{user.username}')
            else:
                print(f"User not found")
        else:
            print(f"Bookitem not found")

