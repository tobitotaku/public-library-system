import json
from enum import Enum

from ast import Pass
import json
from multiprocessing.spawn import prepare

# itemType = Enum("itemType", "book magazine")
class Book:

    def __init__(self, *args):
        # print("inside Book: " )
        # print(args)
        if len(args) > 2:
            self.author = args[0]
            self.title = args[1]
            self.ID = args[2]
            self.ISBN = args[3]

        else:
            self.author = args[0]['author']
            self.title = args[0]['title']
            self.ID = args[0]['ID']
            self.ISBN = args[0]['ISBN']


    def toHeader(self):
        return ["author", "title", "ID", "ISBN"]

    def toRow(self):
        return {"author" : self.author, "title" : self.title, "ID" : self.ID, "ISBN" : self.ISBN}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)


class BookItem:

    def __init__(self, *args):
        # print("inside Book: " )
        # print(args)
        if len(args) > 2:
            self.book = args[0][1]
            self.itemId = args[0][2]
            self.itemType = args[0][3]

        else:
            self.book = args[0]['book']
            self.itemId = args[0]['itemId']
            self.itemType = args[0]['itemType']

    def toHeader(self):
        return ["book", "itemId", "itemType"]

    def toRow(self):
        return {"book" : self.book, "itemId" : self.itemId, "itemType" : self.itemType}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)




#TODO can this be removed?
class Person:
    def __init__(self, *args):
        # print(args)
        if len (args) == 0:
            return
        if len(args) > 3:
            self.username = args[0]
            self.surname = args[1]
            self.age = args[2]
            self.password = args[3]
            self.role = args[4] if 4 in args else 'member'
        else:
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
            self.role = args[0]['role'] if args[0]['role'] else 'member'
        # self.role = 'member'

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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



    # def validate(self, username):
    #     user = self.findbyname(username)
    #     return user

class Member(Person):
    Pass
    
class LibraryAdmin(Person):
    def __init__ (self, *args):
        Person.__init__(self, *args)
        self.role = 'admin'
