# entrypoint of the application
# from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Book, LibraryAdmin, Person, Member
from catalog import Catalog
# from usermodels import LibraryAdmin, Person, Member
from controllers import *
from backup import Backup

# resolver = DataResolver()
# m = [
#     LibraryAdmin("admin", "admin", 33, "admin123"),
#     Member("Jessin", "rodenburg", 33, "test123"),
#     Member("tobi", "roessingh", 33, "test123"),
# ]
# DataResolver.Save(resolver, m, TargetFile.Member)
    # Member("JOhnny", "rodenburg", 33),
    # Member("Eric", "rodenburg", 33),
# ]
# x = Member("Dirk", "De vries", 17)
# books = Book("J.K. Rowling", "harry potter 1")

# backupController = Backup()
# # backupController.StoreBackup()



# backupOptions = backupController.readBackupsAvailable()
# print(backupOptions)


# backupController.listBackupsAvailableForUser()
# listed = backupController.readBackupsAvailable()
# # listed
# data = backupController.loadBackup(listed[7])
# print(data[0])

# DataResolver.Save(resolver, m, TargetFile.Member)

# login, menu navigation, add users
# cv = ControllerView()
cv = UsersCV()

# booksCatalog = Catalog()
# search = booksCatalog.search("5")
# for s in search:
#     print (s.toRow())

# DataResolver.save(resolver, books, TargetFile.Book)

# test = DataResolver.Read(resolver, TargetFile.Member, Member)
