

from ast import Pass
from multiprocessing.spawn import prepare
from datahelpers import DataResolver, JSONDataLayer, TargetFile

class Person:
    def __init__(self, *args):
        if len(args) > 2:
            self.username = args[0]
            self.surname = args[1]
            self.age = args[2]
            self.password = args[3]

        else:
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
        self.role = 'member'

    def toHeader(self):
        return ["username", "surname", "age", "password", "role"]

    def toRow(self):
        return {
            "username" : self.username,
            "surname" : self.surname,
            "age" : self.age,
            "password": self.password,
            "role": self.role,
        }

    @staticmethod
    def all():
        resolver = DataResolver()
        list = DataResolver.Read(resolver, TargetFile.Member, Person)
        return list

    @staticmethod
    def findbyname(username):
        user = False
        list = Person.all()
        if list:
            for item in list:
                if item.username == username:
                    return item
        return user
    
    def add(self):
        list_users = Person.all()
        DataResolver.Save(resolver, list_users, TargetFile.Member)

    # def validate(self, username):
    #     user = self.findbyname(username)
    #     return user

class Member(Person):
    Pass
    
class LibraryAdmin(Person):
    def __init__ (self, *args):
        Person.__init__(self, *args)
        self.role = 'admin'
