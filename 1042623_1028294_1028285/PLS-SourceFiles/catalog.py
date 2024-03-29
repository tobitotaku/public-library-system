from models import Book, BookItem, LoanItem, Person
from datetime import date
from datahelpers import DataResolver, TargetFile
import re
import json
from utils import getNewId, getNewIdTarget
from enum import Enum
import os
from os.path import exists
BookStatus = Enum("loanStatus", "Available Loaned")
itemStatus = Enum("itemStatus", "available loaned")

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
        self.listAllBooks()
        book = None
        if id < len(self.allBooks):
            book = self.allBooks[id]
            # for item in self.listAllBooks():
            #     if int(item.id) == int(id):
            #         return item
        return book

    def getBookByName(self, name):
        self.getBooks()
        if self.listAllBooks():
            for item in self.allBooks:
                if name.lower() == item.title.lower():
                    return item
        return False

    def addBook(self, Author, Title, ISBN) :
        id = getNewIdTarget(TargetFile.Book.name)
        book = Book(id, Author, Title, ISBN)
        self.listAllBooks()
        self.allBooks.append(book)
        for x in range(3):
            self.addBookItem(book)
        self.resolver.Save(self.allBooks, TargetFile.Book)
        return book


    def addBookItem(self, book) :
        id = getNewIdTarget(TargetFile.LibraryItem.name)
        bookitem = BookItem(id, None,book)
        self.listAllBookItems()
        self.allItems.append(bookitem)
        self.save()
        return bookitem


    # TODO test and improve this
    def UpdateBook(self, id, book ) :
        if self.listAllBooks():
            # for i,item in enumerate(self.allBooks):
                if id < len(self.allBooks):
                    self.allBooks[id] = book
                    self.save()
                    self.listAllBookItems()
                    for j,bookitem in enumerate(self.allItems):
                        if bookitem.id == book.id:
                            self.allItems[j].author = book.author
                            self.allItems[j].title = book.title
                            self.allItems[j].ISBN = book.ISBN
                    self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                    return book
        return False
    
    def delete(self, id):
        if self.listAllBooks():
            # for i,item in enumerate(self.allBooks):
                if id < len(self.allBooks):
                    del self.allBooks[id]
                    self.resolver.Save(self.allBooks, TargetFile.Book)
                    return id
        return False

    def deleteBookitem(self, id):
        if self.listAllBookItems():
            # for i,item in enumerate(self.allItems):
                if id < len(self.allItems):
                    del self.allItems[id]
                    self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                    return id
        return False

    def updateBookitem(self, id, bookitem):
        if self.listAllBookItems():
        # for i,item in enumerate(self.allItems):
            if id < len(self.allItems):
                self.allItems[id] = bookitem
                self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                return bookitem
        return False

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
        self.listAllBooks()
        for book in  self.allBooks :
            book : Book
            if id == book.getId() :
                return book

    def getBookItem(self, id):
        self.listAllBookItems()
        item =  None
        if id < len(self.allItems):
            item = self.allItems[id]
        # for item in  self.allItems :
        #     item : BookItem
        #     if id == item.getId():
        #         return item
        return item
        
    def getBookItemById(self, id):
        self.listAllBookItems()
        for bookitem in  self.allItems :
            if id == bookitem.bookItemId :
                return bookitem

    def updateBookitemByBookItem(self, bookitem):
        if self.listAllBookItems():
            for i,item in enumerate(self.allItems):
                if bookitem.bookItemId == item.bookItemId:
                    self.allItems[i] = bookitem
                    self.resolver.Save(self.allItems, TargetFile.LibraryItem)
                    return bookitem
        return False

    def search(self, query) :
        ret = list()
        self.listAllBooks()
        for book in  self.allBooks :
            if re.match(query, book.author + book.title + book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            # elif re.search(query, book.id, re.IGNORECASE) :
                # ret.append(book)
                # return book
            # elif re.search(query, book.title, re.IGNORECASE) :
            #     ret.append(book)
                # return book
            # elif re.search(query, book.ISBN, re.IGNORECASE) :
            #     ret.append(book)
                # return book
        return ret

    def searchBookItem(self, query) :
        ret = list()
        self.listAllBookItems()
        for book in self.allItems :
            if re.search(query, book.author + book.title + book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            # elif re.search(query, book.id, re.IGNORECASE) :
                # ret.append(book)
                # return book
            # elif re.search(query, book.title, re.IGNORECASE) :
            #     ret.append(book)
                # return book
            # elif re.search(query, book.ISBN, re.IGNORECASE) :
            #     ret.append(book)
                # return book
        return ret

    def bulkAddBooks(self, filename):
        notadded = []
        try:
            importlist = self.resolver.jsonResolver.ReadFromFileName(filename, Book)
        except:
            print('Incorrect JSON Format in importfile!')
            return notadded
        self.listAllBooks()
        for i,item in enumerate(importlist):
            book = self.getBookByName(item.title)
            if book:
                notadded.append(item)
            else:
                importlist[i].id = getNewIdTarget(TargetFile.Book.name)
                self.allBooks.append(importlist[i])
                for x in range(3):
                    self.addBookItem(item)
                self.resolver.Save(self.allBooks, TargetFile.Book)
        return notadded
        
    def readImportAvailable(self):
        options = []
        if not exists('./data/import/'):
            os.mkdir('./data/import/')
        for file in os.listdir("./data/import"):
            if re.search('.json$', file, re.IGNORECASE):
                options.append(os.path.join("./data/import/", file))
        return options
