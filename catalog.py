from models import Book, BookItem, LoanItem
from datahelpers import DataResolver, TargetFile
import re
import json
from utils import getNewId

class Catalog:
    
    allBooks = list()
    allItems = list()
    allLoanedItems = list()

    def __init__ (self):
        self.resolver = DataResolver()
        self.allBooks = self.resolver.Read( TargetFile.Book, Book)
        self.allItems = self.resolver.Read( TargetFile.LibraryItem, BookItem)
        self.allLoanedItems = self.resolver.Read( TargetFile.LoanItem, LoanItem)
        # return


    def getBooks(self):
        # print(self.allBooks.)
        return self.allBooks
        # return json.dumps(self.allBooks)

    def getBookItems(self):
        return self.allItems

    def findbyid(self, id):
        self.getBooks()
        if self.allBooks:
            for item in self.allBooks:
                if item.id == id:
                    return item
        return False

    def findbyname(self, name):
        self.getBooks()
        if self.allBooks:
            for item in self.allBooks:
                if item.title == name:
                    return item
        return False

    def addBook(self, Author, Title, ISBN) :
        id = getNewId(self.allBooks)
        book = Book(id, Author, Title, ISBN)
        self.allBooks.append(book)
        self.resolver.Save(self.allBooks, TargetFile.Book)
        return book


    def addBookItem(self, id, Author, Title, ISBN) :
        self.allBooks.append(Book(id, Author, Title, ISBN))
        return


    # TODO test and improve this
    def UpdateBook(self, id, book ) :
        if self.allBooks:
            for i,item in enumerate(self.allBooks):
                if item.id == id:
                    self.allBooks[i] = book
                    self.resolver.Save(self.allBooks, TargetFile.Book)
                    return book
        return False
    
    def delete(self, id):
        if self.allBooks:
            for i,item in enumerate(self.allBooks):
                if item.id == id:
                    del self.allBooks[i]
                    self.resolver.Save(self.allBooks, TargetFile.Book)
                    return id

    def listAllBooks(self):
        return self.allBooks

    def listAllBookItems(self):
        return self.allItems

    def save(self):
        self.resolver.Save(self, self.allBooks, TargetFile.Book)
        self.resolver.Save(self, self.allItems, TargetFile.LibraryItem)


    def get(self, id):
        for book in  self.allBooks :
            if re.search(id, book.id, re.IGNORECASE) :
                return book

    def search(self, query) :
        ret = list()
        for book in  self.allBooks :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.id, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)
                # return book
        return ret

    # TODO lend book item functionality


    

    # TODO All BookItems functionliatieo

    # TODO To search a book item and its availability in the catalog
    # TODO To lend a book item to a member

    # TODO Return a loaned item