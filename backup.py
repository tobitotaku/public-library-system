from datahelpers import DataResolver, TargetFile
from models import Book, Person, LoanItem, BookItem
from catalog import Catalog
from userManager import UserManager
from loanManager import LoanManager
# from usermodels import Person

import os

class Backup:

    ## TODO do this on startup
    def __init__(self):
        self.helper : DataResolver = DataResolver()
        


    # data consists of:
    def StoreBackup(self):
        books : Catalog = Catalog()
        allUsers : list() = UserManager().all()
        allLoanItems : list() = LoanManager(books).allLoanedItems

        
        to_store = {
            "books" : [b.toRow() for b in books.allBooks],
            "libraryItems": [m.toRow() for m in books.allItems],
            "members" : [m.toRow() for m in allUsers],
            "loanitems" : [m.toRow() for m in allLoanItems]
        }
        
        self.helper.Save( object= to_store,target= TargetFile.Backup)


        
    def loadBackup(self, file):
        data = self.helper.ReadBackup( file)
        if len(data) < 3:
            return False
        if not self.helper.Save(data[0], TargetFile.Member):
            return False
        if not self.helper.Save(data[1], TargetFile.Book):
            return False
        if not self.helper.Save(data[2], TargetFile.LibraryItem):
            return False
        if not self.helper.Save(data[3], TargetFile.LoanItem):
            return False


        return True

    
    def readBackupsAvailable(self):
        options = []
        for file in os.listdir("./data/backups"):
            # options.append(file)
            options.append(os.path.join("./data/backups/", file))
        return options

    def listBackupsAvailableForUser(self):
        backups = self.readBackupsAvailable()
        for i in  range(len(backups)):
            print( str(i) + ": " + backups[i])
