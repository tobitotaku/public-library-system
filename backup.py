from datahelpers import DataResolver, TargetFile
from models import Book, Person
from catalog import Catalog
from userManager import UserManager
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
        
        to_store = {
            "books" : [b.toJSON() for b in books.allBooks],
            "libraryItems": [m.toJSON() for m in books.allItems],
            "members" : [m.toJSON() for m in allUsers]
        }
        
        self.helper.Save( object= to_store,target= TargetFile.Backup)


        
    def loadBackup(self, file):
        return self.helper.ReadBackup( file)

    
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
