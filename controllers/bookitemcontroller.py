from controllers.controllers import ControllerView
from controllers.catalogcontroller import CatalogMemberCV

class BookItemCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            (self.render_edit, "Edit"),
            (self.render_delete, "Delete"),
            (self.render_search, "Search"),
            (exit, "Exit application"),
        ]
    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_menu(self):
        self.line()
        print("Bookitem management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        self.line()
        self.render_list_catalog()        
        id = input("[0] bookid? ")

        book = self.catalog.getBookById(id)
        if book:
            self.catalog.addBookItem(id)
        else:
            print('Book not found')
    
    def render_list_catalog(self):
        CatalogMemberCV(ControllerView).render_list()

    def render_list(self):
        self.line()
        print('list of active members')
        print('- ID - bookid - Author - Title - ISBN -')
        if len(self.catalog.allItems) == 0:
            print('Empty list.')
        for item in self.catalog.allItems:
            book = self.catalog.getBookById(item.bookid)
            print(f'- {item.id} - {item.bookid} - {book.author} - {book.title} - {book.ISBN} -')

    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()

        book = self.catalog.getBookItem(id)
        if book:
            confirm, book = self.edit_form(book)
            if confirm:
                self.catalog.update(id, book)
                print(f"Bookitem {book.id} was changed succesfully")
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
                self.usermanager.delete(id)
                print(f"Bookitem {bookitem.id} was deleted succesfully")
            else:
                print(f"Bookitem {bookitem.id} was NOT deleted")
        else:
            print('Bookitem not found')
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author, ISBN: '))
        res = self.catalog.search(query)
        if len(res) > 0:
            print(res)
        else:
            print('No Books found')

    def render_loan(self):
        pass
