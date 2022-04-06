from models import Book, BookItem
from datahelpers import DataResolver, TargetFile
import re
import json

class Catalog:
    
    allBooks = list()
    allItems = list()

    def __init__ (self):
        self.resolver = DataResolver()
        self.allBooks = self.resolver.Read( TargetFile.Book, Book)
        self.allItems = self.resolver.Read( TargetFile.LibraryItem, BookItem)
        # return


    def getBooks(self):
        # print(self.allBooks.)
        return json.dumps(self.allBooks)
    

    def addBook(self, ID, Author, Title, ISBN) :
        self.allBooks.append(Book(ID, Author, Title, ISBN))
        return

    def addBookItem(self, ID, Author, Title, ISBN) :
        self.allBooks.append(Book(ID, Author, Title, ISBN))
        return

    def UpdateBook(self, ID, Author, Title, ISBN ) :
        book = self.get(ID)
        print(book)
        book.author = Author
        book.title  = Title
        book.ISBN = ISBN
        return book

    def save(self):
        self.resolver.Save(self, self.allBooks, TargetFile.Book)
        self.resolver.Save(self, self.allItems, TargetFile.LibraryItem)


    def get(self, id):
        for book in  self.allBooks :
            if re.search(id, book.ID, re.IGNORECASE) :
                return book

    def search(self, query) :
        ret = list()
        for book in  self.allBooks :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ID, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)
                # return book
        return ret
