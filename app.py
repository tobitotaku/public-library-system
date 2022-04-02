# entrypoint of the application
from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Member, Book


resolver = DataResolver()
m = [
    Member("Jessin", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("Eric", "rodenburg", 33),

]
x = Member("Dirk", "De vries", 17)
books = Book("J.K. Rowling", "harry potter 1")



DataResolver.save(resolver, m, TargetFile.Member)

DataResolver.save(resolver, books, TargetFile.Book)

