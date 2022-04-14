from controllers.controllers import ControllerView


class CatalogMemberCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_search, "Search"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_list(self, allBooks = None):
        self.line()
        print('Catalog list')
        print('- ID - Author - Title - ISBN -')
        if not allBooks:
            allBooks = self.catalog.allBooks
        if len(allBooks) == 0:
            print('Empty list.')
        for item in allBooks:
            print('- {id} - {author} - {title} - {ISBN} -'.format(**item.__dict__))
        return self.usermanager.users
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author, ISBN: '))
        res = self.catalog.search(query)
        self.render_list(res)

    def render_menu(self):
        self.line()
        print("Catalog management options:")
        ControllerView.render_menu(self)

class CatalogAdminCV(CatalogMemberCV):
    def __init__(self, *args):
        not self.initialized if CatalogMemberCV.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_add, "Add"),
            (self.render_edit, "Edit"),
            (self.render_delete, "Delete"),
            (self.render_import, "Import JSON"),
        ] + self.actions

    def render_add(self):
        self.line()
        print("Enter book information in fields:")
        name = input("1. Title? ")
        # input("confirm? yes[y]/no[n]")

        book = self.catalog.getBookByName(name)
        if book:
            print('Book: {title} already exists'.format(**book.__dict__))
        else:
            book = self.catalog.addBook(
                input("2. Author? "),
                name,
                input("3. ISBN? "),
            )
            print("Book {title} was added succesfully".format(**book.__dict__))
        
    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()

        book = self.catalog.getBookById(id)
        if book:
            book.title = input("1. Title? ")
            book.author = input("2. Author? ")
            book.ISBN = input("3. ISBN? ")
            self.catalog.UpdateBook(id, book)
            print("Book {title} was changed succesfully".format(**book.__dict__))
        else:
            print('Book not found')

    def render_delete(self):
        self.line()
        self.render_list()
        try:
            id = int(input("Enter ID: "))
        except:
            print("Invalid ID entered. Retry.")
            self.render_delete()
        book = self.catalog.getBookById(id)
        if book:
            is_confirm = input("confirm delete? (y/Enter) ")
            if is_confirm == 'y':
                self.catalog.delete(id)
                print("Book {title} was deleted succesfully".format(**book.__dict__))
            else:
                print("Book {title} was NOT deleted".format(**book.__dict__))
        else:
            print('Book not found')

    def render_import(self):
        pass

# CatalogAdminCV().render_menu()