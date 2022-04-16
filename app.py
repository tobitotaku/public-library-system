# entrypoint of the application
# from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile
from loanManager import LoanManager
from userManager import UserManager
from utils import getNewId
from models import Book, BookItem, LibraryAdmin, Person, Member
from catalog import Catalog
# from usermodels import LibraryAdmin, Person, Member
from controllers.maincontroller import *
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


catalog = Catalog()

loanManger = LoanManager(catalog)
userManager = UserManager()
user : Person = userManager.findbyname("jessin")
print(user.toRow())
# print("-----------------------------------------")
# print(userManager.all())
# for u in userManager.all():
#     us : Person = u
#     print(us.username)

# print(catalog.listAllBookItems())
allItems = catalog.listAllBookItems()
# loanManger.loanItemToMember(user, allItems[0])
# loanManger.setLoanedItemsReceivedById(3)
# print("-----------------------------------------")
# print("Loaned items!")

# loanManger.loanItemToMember(user, allItems[2])
itemsLoaned = loanManger.getCompleteBookItemLoanedByUserId(user.getId())


searchRes = loanManger.searchBookItemWithAvailability("harry")

# searchRes = catalog.search("dune")

# for item in allItems:
#     item : BookItem 
#     print(item.toRow())
#     bookitem : BookItem = catalog.getBookItemByBook(item.bookid)

#     book : Book = catalog.getBookById(bookitem.bookid)
#     print(book)
#     print(book.toRow())

# print("-----------------------------------------")
# print(itemsLoaned)
for item in searchRes:
    # item : BookItem 
    print(item[0].title, item[1].toRow(), item[2])


    # bookitem : BookItem = catalog.getBookItemByBook(item.bookid)
    # book : Book = catalog.getBookById(bookitem.bookid)
    # print(book.toRow())

# loanManger.setLoanedItemsReceivedById(0)

# loanManger.loanItemToMember(user, )

# print(user.surname)

# backupOptions = backupController.readBackupsAvailable()
# print(backupOptions)


# backupController = Backup()
# backupController.StoreBackup()


# backupController.listBackupsAvailableForUser()
# listed = backupController.readBackupsAvailable()
# # listed
# data = backupController.loadBackup(listed[7])
# print(data[0])

# DataResolver.Save(resolver, m, TargetFile.Member)

# login, menu navigation, add users
# MainCV().render_menu()

# print(getNewId(booksCatalog.getBooks()))
# search = booksCatalog.search("5")
# for s in search:
#     print (s.toRow())

# DataResolver.save(resolver, books, TargetFile.Book)

# test = DataResolver.Read(resolver, TargetFile.Member, Member)
