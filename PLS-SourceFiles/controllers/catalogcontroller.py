from controllers.controllers import ControllerView
from utils import *
import sys

class CatalogMemberCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List all books"),
            (self.render_search, "Search a book"),
            (self.render_main, "Back to main menu"),
            (self.exit, "Exit application"),
        ]

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_list(self, allBooks = None):
        # print('Catalog list')
        # print('- ID - Author - Title - ISBN -')
        # if not allBooks:
        #     allBooks = self.catalog.listAllBooks()
        # if len(allBooks) == 0:
        #     print('Empty list.')
        # for item in allBooks:
        #     print(f'- {item.id} - {item.author} - {item.title} - {item.ISBN} -')
        # return self.usermanager.users

        self.line()
        print('Books in Catalog.')
        # allBooks = self.catalog.listAllBooks()
        print(f'{s("#", 3)} - {s("Title")} - {s("Author")} - {s("ISBN")}')
        if not allBooks:
            allBooks = self.catalog.listAllBooks()
        if len(allBooks) == 0:
            print('Empty list.')
        for i,item in enumerate(allBooks):
            print(f"{s(i, 3)} - {s(item.title)} - {s(item.author)} - {s(item.ISBN)}")
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author: '))
        res = self.catalog.search(query)
        self.render_list(res)

    def render_menu(self):
        self.line()
        self.catalog.listAllBooks()
        print("Catalog management options:")
        ControllerView.render_menu(self)

class CatalogAdminCV(CatalogMemberCV):
    def __init__(self, *args):
        not self.initialized if CatalogMemberCV.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_add, "Add a book"),
            (self.render_edit, "Edit a book"),
            (self.render_delete, "Delete a book"),
            (self.render_import_list, "List Imports(JSON)"),
            (self.render_import, "Import Bulk Books(JSON)"),
        ] + self.actions

    def render_add(self):
        self.line()
        print("Enter book information in fields:")
        name = input("[0] Title? ")
        # input("confirm? yes[y]/no[n]")

        book = self.catalog.getBookByName(name)
        if book:
            print(f'Book: {book.title} already exists')
        else:
            book = self.catalog.addBook(
                input("[1] Author? "),
                name,
                input("[2] ISBN? "),
            )
            print(f"Book {book.title} was added succesfully")
        
    def render_edit(self):
        self.render_list()
        id = None
        book = None
        try:
            id = int(input("Enter number from column #: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()
        if len(self.catalog.allBooks) == 0:
            return
        if id and id >=0:
            book = self.catalog.getBookById(id)
        if book:
            confirm, book = self.edit_form(book)
            if confirm:
                self.catalog.UpdateBook(id, book)
                print(f"Book {book.title} was changed succesfully.")
            else:
                print(f"Book {book.title} was NOT changed.")
        else:
            print('Book not found. You\'ll now redirected to Catalog menu')

    def render_delete(self):
        self.line()
        self.render_list()
        id = None
        book = None
        try:
            id = int(input("Enter number from column #: "))
        except:
            print("Invalid number entered. Retry.")
            self.render_delete()
        if len(self.catalog.allBooks) == 0:
            return
        if id and id >=0:
            book = self.catalog.getBookById(id)
        if book:
            is_confirm = input("confirm delete (input:y) or cancel (press:Enter) ?")
            if is_confirm == 'y':
                if self.catalog.delete(id):
                    print(f"Book {book.title} was deleted succesfully")
                else:
                    print(f"Book {book.title} was NOT deleted")
            else:
                print(f"Book {book.title} was NOT deleted")
        else:
            print('Book not found. You\'ll now redirected to Catalog menu')

    def render_import_list(self):
        print('Catalog Available Import Files.')
        importfiles = self.catalog.readImportAvailable()
        print(f'{s("#", 3)} - {s("Files", 40)}')
        if len(importfiles) == 0:
            print('Empty list.')
        for i,item in enumerate(importfiles):
            print(f'{i} - {s(item, 40)}')
        return importfiles

    def render_import(self):
        importlist = self.render_import_list()
        importid = self.select_field_id('Enter a number from column #: ')
        if len(importlist) > importid:
            loadimport = importlist[importid]
            print(f'Importfile [{importid}] {loadimport} selected')
            confirm = input('Confirm loading import (input:y) or cancel (press:Enter)?')
            if confirm == 'y':
                notadded = self.catalog.bulkAddBooks(loadimport)
                print(f'Import [{importid}] {loadimport} loaded')
                for item in notadded:
                    print(f'Book: {item.title} Skipped. Already exists ')
        else:
            print('Import not found')
