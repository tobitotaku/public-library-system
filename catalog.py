from models import Book, BookItem, LoanItem, Person
from datetime import date
from dateutil.relativedelta import relativedelta
from datahelpers import DataResolver, TargetFile
import re
import json
from utils import getNewId
from enum import Enum
import os
BookStatus = Enum("loanStatus", "Available Loaned")


class Catalog:
    
    allBooks = list()
    allItems = list()

    def __init__ (self):
        self.resolver = DataResolver()
        self.listAllBooks()
        self.listAllBookItems()
    
    def getBooks(self):
        # print(self.allBooks.)
        return self.allBooks
        # return json.dumps(self.allBooks)

    def getBookItems(self):
        return self.allItems

    def getBookById(self, id):

        if self.allBooks:
            for item in self.allBooks:
                if int(item.id) == int(id):
                    return item
        return False

    def getBookByName(self, name):
        self.getBooks()
        if self.allBooks:
            for item in self.allBooks:
                if re.search(name, item.title, re.IGNORECASE):
                    return item
        return False

    def addBook(self, Author, Title, ISBN) :
        id = getNewId(self.allBooks)
        book = Book(id, Author, Title, ISBN)
        self.allBooks.append(book)
        self.resolver.Save(self.allBooks, TargetFile.Book)
        return book


    def addBookItem(self, bookid) :
        id = getNewId(self.allItems)
        bookitem = BookItem(id, bookid)
        self.allItems.append(bookitem)
        self.save()
        return bookitem


    # TODO test and improve this
    def UpdateBook(self, id, book ) :
        if self.allBooks:
            for i,item in enumerate(self.allBooks):
                if item.id == id:
                    self.allBooks[i] = book
                    self.save()
                    return book
        return False
    
    def delete(self, id):
        if self.allBooks:
            for i,item in enumerate(self.allBooks):
                if item.id == id:
                    del self.allBooks[i]
                    self.resolver.Save(self.allBooks, TargetFile.Book)
                    return id

    def deleteBookitem(self, id):
        if self.allItems:
            for i,item in enumerate(self.allItems):
                if item.id == id:
                    del self.allItems[i]
                    self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                    return id

    def updateBookitem(self, id, bookitem):
        for i,item in enumerate(self.allItems):
            if item.id == id:
                self.allItems[i] = bookitem
                self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                return bookitem

    def listAllBooks(self):
        self.allBooks = self.resolver.Read( TargetFile.Book, Book)
        return self.allBooks

    def listAllBookItems(self):
        self.allItems = self.resolver.Read( TargetFile.LibraryItem, BookItem)
        return self.allItems

    def save(self):
        self.resolver.Save(self.allBooks, TargetFile.Book)
        self.resolver.Save(self.allItems, TargetFile.LibraryItem)


    def getBook(self, id):
        for book in  self.allBooks :
            book : Book
            if id == book.getId() :
                return book

    def getBookItem(self, id):
        for item in  self.allItems :
            item : BookItem
            if id == item.getId():
                return item

    def getBookItemByBook(self, bookId):
        ret = []
        for item in  self.allItems :
            if int(item.bookid) ==  int(bookId):
                # print(item.bookid, bookId)
                ret.append(item)

        # print(ret)
        return ret

    def search(self, query) :
        ret = list()
        for book in  self.allBooks :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            # elif re.search(query, book.id, re.IGNORECASE) :
                # ret.append(book)
                # return book
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)
                # return book
        return ret

    def bulkAddBooks(self, filename):
        notadded = []
        try:
            importlist = self.resolver.jsonResolver.ReadFromFileName(filename, Book)
        except:
            print('Incorrect JSON Format in importfile!')
            return notadded
        for i,item in enumerate(importlist):
            book = self.getBookByName(item.title)
            if book:
                notadded.append(item)
            else:
                importlist[i].id = getNewId(self.allBooks)
                self.allBooks.append(item)
        self.resolver.Save(self.allBooks, TargetFile.Book)
        return notadded
        
    def readImportAvailable(self):
        options = []
        for file in os.listdir("./data/import"):
            if re.search('.json$', file, re.IGNORECASE):
                options.append(os.path.join("./data/import/", file))
        return options
