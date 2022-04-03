

from ast import Pass
from datahelpers import DataResolver, JSONDataLayer, TargetFile

class Person:
    def __init__(self, *args):
        print("inside Member: " )
        print(args)
        if len(args) > 2:
            self.username = args[0]
            self.surname = args[1]
            self.age = args[2]
            self.password = args[3]
            self.role = args[4]

        else:
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
            self.role = args[0]['role']

    def toHeader(self):
        return ["username", "surname", "age", "password"]

    def toRow(self):
        return {
            "username" : self.username,
            "surname" : self.surname,
            "age" : self.age,
            "password": self.password,
            "role": self.role,
        }

    def all():
        resolver = DataResolver()
        list = DataResolver.Read(resolver, TargetFile.Member, Person)
        return list

    def findbyname(username):
        user = False
        list = Person.all()
        if list:
            for item in list:
                if item.username == username:
                    return item
        return user
    
    # def validate(self, username):
    #     user = self.findbyname(username)
    #     return user

class Member(Person):
    Pass
    # def __init__ (self, *args):
    #     self.role = 'member'
    #     self.surname = surname
    #     self.age = age
    
class LibraryAdmin(Person):
    Pass
    # def __init__ (self, *args):
        # self.username = 'admin'
        # self.password = 'admin123'
        # self.role = 'member'