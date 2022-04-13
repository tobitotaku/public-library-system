from controllers.controllers import ControllerView

class BookItemCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            (self.render_edit, "Edit"),
            (self.render_delete, "Delete"),
            (self.render_search, "Search"),
            (self.render_import, "Import JSON"),
            (exit, "Exit application"),
        ]
    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')

    def render_menu(self):
        self.line()
        print("Catalog management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        self.line()
        print("Enter book information in fields:")
        name = input("1. Title? ")
        # input("confirm? yes[y]/no[n]")

        book = self.catalog.getBookByName(name)
        if book:
            print('Book: {title} already exists'.format(**book.__dict__))
            is_continue = str(input('Would like to a another Book? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_add()
        else:
            book = self.catalog.addBook(
                input("2. Author? "),
                name,
                input("3. ISBN? "),
            )
            print("Book {title} was added succesfully".format(**book.__dict__))
        
        self.render_menu()

    def render_list(self):
        self.line()
        print('Catalog list')
        print('- ID - Author - Title - ISBN -')
        if len(self.catalog.allBooks) == 0:
            print('Empty list.')
        for item in self.catalog.allBooks:
            print('- {id} - {author} - {title} - {ISBN} -'.format(**item.__dict__))
        return self.usermanager.users

    def render_edit(self):
        self.render_list()
        try:
            id = int(input("Select & Edit book by typing their ID: "))
        except:
            print("Invalid option entered. Enter an ID")
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
            is_continue = str(input('Would like to edit another Book? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_edit()

        self.render_menu()

    def render_delete(self):
        self.line()
        self.render_list()
        try:
            id = int(input("Select & Delete a book by typing their ID: "))
        except:
            print("Invalid ID entered. Enter an ID")
            self.render_delete()
        book = self.catalog.getBookById(id)
        if book:
            is_confirm = input("confirm delete? [confirm with: y (for yes) or press Enter]")
            if is_confirm == 'y':
                self.catalog.delete(id)
                print("Book {title} was deleted succesfully".format(**book.__dict__))
            else:
                print("Book {title} was NOT deleted".format(**book.__dict__))
        else:
            print('Book not found')
            is_continue = str(input('Would like to Delete another Book? [confirm with: y (for yes) or press Enter]'))
            if is_continue == 'y':
                self.render_delete()

        self.render_menu()
    
    def render_search(self):
        self.line()
        query = str(input('Search by Title, Author, ISBN: '))
        res = self.catalog.search(query)
        if len(res) > 0:
            print(res)
        else:
            print('No Books found')

    def render_import(self):
        pass

# CatalogCV().render_menu()