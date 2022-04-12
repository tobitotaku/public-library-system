from matplotlib.style import available
from models import Book, BookItem, LoanItem, Person
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

    # TODO All BookItems functionliatieo
    def listAllBookItemsLoaned(self) :
        currentItem : LoanItem
        ret = list()
        for loanItem  in self.allLoanedItems :
            currentItem = loanItem
            currentItem.bookItemId
            bookItem : BookItem = self.catalog.getBookItem(currentItem.bookItemId)
            book = self.catalog.getBook(bookItem.book)
            loaner : Person = self.userManager.findbyid(currentItem.userId)
            ret.append({currentItem, bookItem, book, loaner})
        return ret

    def getCompleteBookItemLoanedById(self, id : int) :
        ret = list()
        currentItem = self.getLoanItemById(id)
        bookItem : BookItem = self.catalog.getBookItem(currentItem.bookItemId)
        book = self.catalog.getBook(bookItem.book)
        loaner : Person = self.userManager.findbyid(currentItem.userId)
        ret.append({currentItem, bookItem, book, loaner})
        return ret

    def getLoanItemsByUserId(self, userId) :
        ret = list()
        if self.allLoanedItems:
            for item in self.allLoanedItems:
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
        return True
        
    def getCompleteBookItemLoanedByUserId(self, user) :
        ret = list()
        items = self.getLoanItemsByUserId(user)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book = self.catalog.getBook(bookItem.book)
            ret.append({items, bookItem, book, user})
        return ret
    
    def searchBookItemWithAvailability(self, query):
        searchRes = self.catalog.search(query)
        ret = list()
        for book in searchRes:
            book : Book
            bookItem : BookItem = self.catalog.getBookItemByBook(book.id)
            # book = self.catalog.getBook(bookItem.book)
            loanItem : LoanItem = self.getCompleteBookItemLoanedById(bookItem.id)            
            if loanItem:
                if loanItem.loanStatus == BookStatus.Available:
                    ret.append({book, bookItem, "available"})
                else:
                    ret.append({book, bookItem, "unavailable"})
            else:
                ret.append({book, bookItem, "available"})

        return ret



    def setLoanedItemsReceived(self, loanItems ) :
        if self.allLoanedItems:
            for L in loanItems:
                for i,item in enumerate(self.allLoanedItems):
                    L : LoanItem
                    if item.id == L.id :
                        item : LoanItem
                        item.loanStatus = BookStatus.Available
                        self.allLoanedItems[i] = item
                        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
                        return item
        return False


    def getLoanItemById(self, id):
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.id == id:
                    return item
        return False


    def loanItemToMember(self, member : Person, itemToLoan : BookItem):
        #add checks for permitting member to borrow the item
        #if (get amount of books currently borrowed >= 3 do not lend):
        returnDate = date.today() + relativedelta(month=+1)
        item : LoanItem = LoanItem(getNewId(self.allLoanedItems), itemToLoan.id, member.id, date.today(), returnDate, BookStatus.Loaned)
        return item

    

    # TODO To search a book item and its availability in the catalog
    def searchLoanItems(self, query) :
        ret = list()
        for book in  self.allLoanedItems :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.id, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)
        return ret
