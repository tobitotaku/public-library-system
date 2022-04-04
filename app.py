# entrypoint of the application
from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Book
from catalog import Catalog
from usermodels import LibraryAdmin, Person, Member
from controllers import *

# resolver = DataResolver()
# m = [
#     LibraryAdmin("admin", "admin", 33, "admin123"),
#     Member("Jessin", "rodenburg", 33, "test123"),
# ]
# DataResolver.Save(resolver, m, TargetFile.Member)

# new_member = Member("tobi", "roessingh", 33, 'test123')
# new_member = Member("JOhnny", "test", 33, 'test123')
# new_member.save()
    # Member("JOhnny", "rodenburg", 33),
    # Member("JOhnny", "rodenburg", 33),
    # Member("Eric", "rodenburg", 33),

# x = Person.all()
# ]
# x = Member("Dirk", "De vries", 17)
# books = Book("J.K. Rowling", "harry potter 1")

# DataResolver.Save(resolver, m, TargetFile.Member)

# login, menu navigation, add users
cv = UsersCV()

# booksCatalog = Catalog()
# search = booksCatalog.search("5")
# for s in search:
#     print (s.toRow())

# DataResolver.save(resolver, books, TargetFile.Book)

# test = DataResolver.Read(resolver, TargetFile.Member, Member)
