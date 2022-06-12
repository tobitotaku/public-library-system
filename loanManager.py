from matplotlib.style import available
from models import Book, BookItem, LoanItem, Member, Person
from datetime import date
from dateutil.relativedelta import relativedelta
from catalog import Catalog
from datahelpers import DataResolver, TargetFile
import re
import json
from userManager import UserManager
from utils import getNewId
from enum import Enum

BookStatus = Enum("loanStatus", "Available Loaned")


class LoanManager:


    # pass it on when instantiating so we don't have to read all data twice.
    def __init__(self, catalog : Catalog):
        self.userManager = UserManager()
        self.resolver = DataResolver()
        self.allLoanedItems = self.resolver.Read( TargetFile.LoanItem, LoanItem)
        self.catalog = catalog

    def listAllBookItemsLoaned(self) :
        currentItem : LoanItem
        ret = list()
        for loanItem  in self.allLoanedItems :
            currentItem = loanItem
            currentItem.bookItemId
            bookItem : BookItem = self.catalog.getBookItem(currentItem.bookItemId)
            book = self.catalog.getBookById(bookItem.bookid)
            loaner : Person = self.userManager.findbyid(currentItem.userId)
            ret.append({"item": currentItem,"bookItem" : bookItem, "book":  book,"user": loaner})
        return ret

    def getCompleteBookItemLoanedById(self, id : int) :
        ret = list()
        currentItem = self.getLoanItemById(id)
        bookItem : BookItem = self.catalog.getBookItem(currentItem.bookItemId)
        book = self.catalog.getBookById(bookItem.bookid)
        loaner : Person = self.userManager.findbyid(currentItem.userId)
        ret.append({currentItem, bookItem, book, loaner})
        return ret

    def getLoanItemsByUserId(self, userId) :
        ret = list()
        
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                item :LoanItem
                if item.userId == userId:
                    ret.append(item)
        return ret

    def getBookItemAvailable(self, bookItemId):
        for loanItem in self.allLoanedItems:
            loanItem : LoanItem
            if loanItem.bookItemId == bookItemId:
                if loanItem.loanStatus == BookStatus.Available:
                    return True
                return False
        return False
        
    def getCompleteBookItemLoanedByUserId(self, user) :
        ret = list()
        items = self.getLoanItemsByUserId(user)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book = self.catalog.getBookById(bookItem.bookid)
            user : Member = self.userManager.findbyid(t.userId)
            ret.append({"item": item,"bookItem" : bookItem, "book":  book,"user": user})
        return ret
    
    def getCompleteBookItemLoanedByBookItemId(self, bookItemId) :
        ret = list()
        items = self.getLoanItemsByBookItemId(bookItemId)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book : Book = self.catalog.getBookById(bookItem.bookid)
            user : Member = self.userManager.findbyid(t.userId)
            ret.append({t, bookItem, book, user})
        return ret

    def getLoanItemsByBookItemId(self, bookItemId) :
        ret = list()
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.bookItemId == bookItemId:
                    ret.append(item)
        return ret

    def searchBookItemWithAvailability(self, query):
        searchRes = self.catalog.search(query)
        # print(searchRes)
        ret = list()
        for book in searchRes:
            # print(book.toRow())
            book : Book
            bookItem = self.catalog.getBookItemByBook(book.getId())
            # print(bookItem)
            # book = self.catalog.getBook(bookItem.book)
            for item in bookItem:
                loanItem : LoanItem = self.getLoanItemsByBookItemId(item.getId())   
                if loanItem:
                    ret.append((book, item, "unavailable"))
                else:
                    ret.append((book, item, "available"))
        return ret

    def getBookItemWithAvailability(self):
        ret = list()
        for item in self.catalog.allItems:
            # print(item)
            loanItem : LoanItem = self.getLoanItemsByBookItemId(item.id)   
            # print(loanItem)
            book : Book = self.catalog.getBookById(item.bookid)   
            if not book:
                ret.append(Book(-1, "unknown", "unknown", "000"))
            # print(book)
            if loanItem:
                ret.append((book, item, "unavailable"))
            else:
                ret.append((book, item, "available"))
        return ret

    def setLoanedItemsReceivedById(self, loanItems ) :
        if not isinstance(loanItems, list):
            loanItems = [loanItems]

        if self.allLoanedItems:
            for L in loanItems:
                for i,item in enumerate(self.allLoanedItems):
                    if item.id == L :
                        del self.allLoanedItems[i]
                        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
                        

    def getLoanItemById(self, id):
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.id == id:
                    return item
        return False


    def loanItemToMember(self, member : Person, itemToLoan : BookItem):
        alreadyLoanedItems = self.getLoanItemsByUserId(member.getId())
        if len(alreadyLoanedItems) >= 3:
            print("user has too many books!")
            return
        #if (get amount of books currently borrowed >= 3 do not lend):
        
        dateObject = date.today()
        # today = dateObject
        returnDate = dateObject +relativedelta(days=+30)
        item : LoanItem = LoanItem(getNewId(self.allLoanedItems), itemToLoan.getId(), member.id, dateObject, returnDate , BookStatus.Loaned.name)
        self.allLoanedItems.append(item)
        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)

    # TODO To search a book item and its availability in the catalog
    def searchLoanItems(self, query) :
        ret = list()
        for book in  self.catalog.allBooks :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.id, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)

        # for b in ret

