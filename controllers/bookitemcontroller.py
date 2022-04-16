from controllers.controllers import ControllerView
from controllers.catalogcontroller import *

class BookItemCV(ControllerView):
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
        self.catalogcv = CatalogAdminCV(ControllerView)

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_menu(self):
        self.line()
        print("Library management options:")
        ControllerView.render_menu(self)

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
    
    def render_list(self):
        self.line()
        print('Bookitems in Library.')
        print('- ID - bookid - Author - Title - ISBN -')
        if len(self.catalog.allItems) == 0:
            print('Empty list.')
        for item in self.catalog.allItems:
            book = self.catalog.getBookById(item.bookid)
            print(f"- {item.id} - {item.bookid} - {book.author} - {book.title} - {book.ISBN} -")

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

