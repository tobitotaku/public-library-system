# entrypoint of the application
from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Book
from usermodels import Person
from controllers import ControllerView

resolver = DataResolver()
m = [
    Person("Jessin", "rodenburg", 33, "test123", "member"),
    Person("admin", "rodenburg", 33, "admin123", "admin"),
    # Member("JOhnny", "rodenburg", 33),
    # Member("JOhnny", "rodenburg", 33),
    # Member("JOhnny", "rodenburg", 33),
    # Member("Eric", "rodenburg", 33),

]
# x = Member("Dirk", "De vries", 17)
# books = Book("J.K. Rowling", "harry potter 1")



DataResolver.Save(resolver, m, TargetFile.Member)

# DataResolver.save(resolver, books, TargetFile.Book)

# test = DataResolver.Read(resolver, TargetFile.Member, Member)

cv = ControllerView()