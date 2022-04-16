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

    # TODO All BookItems functionliatieo
    def listAllBookItemsLoaned(self) :
        currentItem : LoanItem
        ret = list()
        for loanItem  in self.allLoanedItems :
            currentItem = loanItem
            currentItem.bookItemId
            bookItem : BookItem = self.catalog.getBookItem(currentItem.bookItemId)
            book = self.catalog.getBookById(bookItem.bookid)
            loaner : Person = self.userManager.findbyid(currentItem.userId)
            ret.append({currentItem, bookItem, book, loaner})
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
        # print(items)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book = self.catalog.getBook(bookItem.bookid)
            ret.append({"items": items,"bookItem" : bookItem, "book":  book,"user": user})
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
        ret = list()
        for book in searchRes:
            book : Book
            bookItem : BookItem = self.catalog.getBookItemByBook(book.id)
            # book = self.catalog.getBook(bookItem.book)
            loanItem : LoanItem = self.getCompleteBookItemLoanedByBookItemId(bookItem.id)            
            if loanItem:
                if loanItem.loanStatus == BookStatus.Available:
                    ret.append({book, bookItem, "available"})
                else:
                    ret.append({book, bookItem, "unavailable"})
            else:
                ret.append({book, bookItem, "available"})

        return ret



    def setLoanedItemsReceived(self, loanItems ) :
        if not isinstance(loanItems, list):
            loanItems = [loanItems]

        if self.allLoanedItems:
            for L in loanItems:
                for i,item in enumerate(self.allLoanedItems):
                    L : LoanItem
                    if item.id == L.id :
                        del self.allLoanedItems[i]
                        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
                        return item.id
        return False

    def setLoanedItemsReceivedById(self, loanItems ) :
        if not isinstance(loanItems, list):
            loanItems = [loanItems]

        if self.allLoanedItems:
            for L in loanItems:
                for i,item in enumerate(self.allLoanedItems):
                    if item.id == L :
                        del self.allLoanedItems[i]
                        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
                        
        return False



    def getLoanItemById(self, id):
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.id == id:
                    return item
        return False


    def loanItemToMember(self, member : Person, itemToLoan : BookItem):
        # TODO add checks for permitting member to borrow the item
        alreadyLoanedItems = self.getLoanItemsByUserId(member.getId())
        print(alreadyLoanedItems)
        if len(alreadyLoanedItems) > 3:
            print("user has too many books!")
            return
        #if (get amount of books currently borrowed >= 3 do not lend):
        
        print(date.today())
        dateObject = date.today()
        # today = dateObject
        returnDate = dateObject +relativedelta(days=+30)
        item : LoanItem = LoanItem(getNewId(self.allLoanedItems), itemToLoan.getId(), member.id, dateObject, returnDate , BookStatus.Loaned.name)
        self.allLoanedItems.append(item)
        print(self.allLoanedItems[0].returnDate)
        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)


    def add(self, member : Person, itemToLoan : BookItem):
        item = self.loanItemToMember(member, itemToLoan)
        self.allLoanedItems.append(item)
        self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
        return item


        

    

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
        return ret



