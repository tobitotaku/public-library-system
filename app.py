# entrypoint of the application
from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile

from models import Member


# class app:
    # def __init__(self):
        # 


resolver = DataResolver()
m = [
    Member("Jessin", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("JOhnny", "rodenburg", 33),
    Member("Eric", "rodenburg", 33),

]
x = Member("Dirk", "De vries", 17)
DataResolver.save(resolver, x, TargetFile.Member)
