# entrypoint of the application
from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Member, Book
from catalog import Catalog

resolver = DataResolver()
# m = [
#     Member("Jessin", "rodenburg", 33),
#     Member("JOhnny", "rodenburg", 33),
#     Member("JOhnny", "rodenburg", 33),
#     Member("JOhnny", "rodenburg", 33),
#     Member("Eric", "rodenburg", 33),

# ]
# x = Member("Dirk", "De vries", 17)
# books = Book("J.K. Rowling", "harry potter 1")



# DataResolver.Save(resolver, m, TargetFile.Member)

booksCatalog = Catalog()
search = booksCatalog.search("5")
for s in search:
    print (s.toRow())

# DataResolver.save(resolver, books, TargetFile.Book)

# test = DataResolver.Read(resolver, TargetFile.Member, Member)

# print(x.toRow())
# print(test[1].toRow())