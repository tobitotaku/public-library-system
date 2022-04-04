from models import Book
from datahelpers import DataResolver, TargetFile
import re

class Catalog:
    
    allBooks = list()

    def __init__ (self):
        self.allBooks = DataResolver.Read(self, TargetFile.Book, Book)
        # return


    def addBook(self, ID, Author, Title, ISBN) :
        self.allBooks.append(Book(ID, Author, Title, ISBN))
        return

    def UpdateBook(self, ID, Author, Title, ISBN ) :
        book = self.search(ID)
        print(book)
        book.author = Author
        book.title  = Title
        book.ISBN = ISBN
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
