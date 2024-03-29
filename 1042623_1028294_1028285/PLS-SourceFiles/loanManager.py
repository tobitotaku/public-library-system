from matplotlib.style import available
from models import Book, BookItem, LoanItem, Member, Person, itemStatus
from datetime import date
from dateutil.relativedelta import relativedelta
from catalog import Catalog
from datahelpers import DataResolver, TargetFile
import re
import json
from userManager import UserManager
from utils import getNewId, getNewIdTarget
from enum import Enum

BookStatus = Enum("loanStatus", "Available Loaned")


class LoanManager:


    # pass it on when instantiating so we don't have to read all data twice.
    def __init__(self, catalog : Catalog):
        self.userManager = UserManager()
        self.resolver = DataResolver()
        self.allLoanedItems = self.resolver.Read( TargetFile.LoanItem, LoanItem)
        self.catalog = catalog

    def load(self):
        self.allLoanedItems = self.resolver.Read( TargetFile.LoanItem, LoanItem)

    def listAllBookItemsLoaned(self) :
        ret = list()
        self.load()
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.itemStatus == itemStatus.loaned.name:
                    ret.append(item)
        return ret

    def getLoanItemsByUserId(self, userId) :
        ret = list()
        self.load()
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.userid == userId and item.itemStatus == itemStatus.loaned.name:
                    ret.append(item)
        return ret

        
    def getCompleteBookItemLoanedByUserId(self, user) :
        ret = list()
        items = self.getLoanItemsByUserId(user)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book = self.catalog.getBookById(bookItem.id)
            user : Member = self.userManager.findbyid(t.userId)
            ret.append({"item": item,"bookItem" : bookItem, "book":  book,"user": user})
        return ret
    
    def getCompleteBookItemLoanedByBookItemId(self, bookItemId) :
        ret = list()
        items = self.getLoanItemsByBookItemId(bookItemId)
        for item in items:
            t : LoanItem = item
            bookItem : BookItem = self.catalog.getBookItem(t.bookItemId)
            book : Book = self.catalog.getBookById(bookItem.id)
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

    def getBookItemsAvailable(self):
        self.catalog.listAllBookItems()
        res = []
        if len(self.catalog.allItems) == 0:
            res = False
        for i, item in enumerate(self.catalog.allItems):
            if item.itemStatus == itemStatus.available.name:
                res.append(item)
        return res

    def getBookItemAvailable(self, id):
        self.getBookItemsAvailable()
        item =  None
        if id < len(self.allItems):
            item = self.allItems[id]
        # for item in  self.allItems :
        #     item : BookItem
        #     if id == item.getId():
        #         return item
        return item

    def setLoanedItemsReceivedById(self, loanitemid , userid) :
        useritems = self.getLoanItemsByUserId(userid)
        selecteditem = None
        if loanitemid < len(useritems):
            selecteditem = useritems[loanitemid]
        
        if selecteditem is None:
            print("Incorrect LoanItemID entered.")
            return (False, None)
        user = self.userManager.findbyid(userid)
        if user is None:
            print("User not found.")
            return (False, None)

        self.load()
        if self.allLoanedItems:
            for i,item in enumerate(self.allLoanedItems):
                if item.loanItemid == selecteditem.loanItemid and item.userid == userid:
                    self.allLoanedItems[i].itemStatus = itemStatus.returned.name
                    self.catalog.listAllBookItems()
                    bookitem = self.catalog.getBookItemById(item.bookItemId)
                    bookitem.itemStatus = itemStatus.available.name
                    self.catalog.updateBookitemByBookItem(bookitem)
                    self.resolver.Save(self.allLoanedItems, TargetFile.LoanItem)
                    return (True, item)
        return (False, None)
                        

    def getLoanItemById(self, id):
        if self.allLoanedItems:
            for item in self.allLoanedItems:
                if item.id == id:
                    return item
        return False

    def loanItemToMember(self, member : Person, itemToLoan : BookItem):
        alreadyLoanedItems = self.getLoanItemsByUserId(member.getId())
        if len(alreadyLoanedItems) >= 3:
            print(f"Only a maximum of 3 books can be borrowed. Please return some books before borrowing.")
            return False
        for i, item in enumerate(alreadyLoanedItems):
            if (itemToLoan.id == item.id):
                print(f"Member {member.username} has already borrowed this book!")
                return False
        dateObject = date.today()
        returnDate = dateObject +relativedelta(days=+30)
        itemToLoan.itemStatus = itemStatus.loaned.name
        self.catalog.updateBookitemByBookItem(itemToLoan)
        item = LoanItem(getNewIdTarget(TargetFile.LoanItem.name), dateObject, returnDate, itemToLoan, member)
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

        # for b in ret

