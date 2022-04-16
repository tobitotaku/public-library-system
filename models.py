import json
from enum import Enum
from utils import getNewId
from ast import Pass
import json
# import datetime
from datetime import datetime
from multiprocessing.spawn import prepare

# itemType = Enum("itemType", "book magazine")
itemStatus = Enum("itemStatus", "available loaned")
class Book:

    def __init__(self, *args):
        if len(args) > 2:
            self.id = args[0]
            self.author = args[1]
            self.title = args[2]
            self.ISBN = args[3]

        else:
            self.id = args[0]['id']
            self.author = args[0]['author']
            self.title = args[0]['title']
            self.ISBN = args[0]['ISBN']

    def getId(self):
        return self.id

    def toHeader(self):
        return ["id","author", "title",  "ISBN"]

    def toRow(self):
        return { "id" : self.id, "author" : self.author, "title" : self.title, "ISBN" : self.ISBN}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)


class BookItem:

    def __init__(self, *args):
        if len(args) > 1:
            self.id = args[0]
            self.bookid = args[1]
            self.itemStatus = args[2] if len(args) > 2 else itemStatus.available.value

        else:
            self.id = args[0]['id']
            self.bookid = args[0]['bookid']
            self.itemStatus = args[0]['itemStatus']
    
    def getId(self):
        return self.id

    def toHeader(self):
        return ["id","bookid", "itemStatus"]

    def toRow(self):
        return {"id" : self.id, "bookid" : self.bookid, "itemStatus" : self.itemStatus}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)

class LoanItem:
    def __init__(self, *args):
        print(args)
        if len(args) > 2:
            self.id = args[0]
            self.bookItemId = args[1]
            self.userId = args[2]
            self.issueDate = args[3]
            self.returnDate = args[4]
            self.loanStatus = args[5]

        else:
            self.id = args[0]['id']
            self.bookItemId = args[0]['bookItemId']
            self.userId = args[0]['userId']
            self.issueDate = datetime.strptime(args[0]['issueDate'], "%d-%m-%Y")
            self.returnDate = datetime.strptime(args[0]['returnDate'], "%d-%m-%Y")
            self.loanStatus = "Loaned"
    def getId(self):
        return self.id

    def toHeader(self):
        return ["id", "bookItemId", "userId", "issueDate", "returnDate", "loanStatus"]

    def toRow(self):
        return { "id" : self.id, "bookItemId" : self.bookItemId, "userId" : self.userId, "issueDate" : self.issueDate, "returnDate" : self.returnDate, "loanStatus" : self.loanStatus}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    
        


class Person:
    def __init__(self, *args):
        if len (args) == 0:
            return
        if len(args) > 3:
            self.id = args[0]
            self.username = args[1]
            self.surname = args[2]
            self.age = args[3]
            self.password = args[4]
            self.role = args[5] if 5 in args else 'member'
        else:
            self.id = args[0]['id']
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
            self.role = args[0]['role'] if args[0]['role'] else 'member'

    def getId(self):
        return self.id

    def toHeader(self):
        return ["id", "username", "surname", "age", "password", "role"]

    def toRow(self):
        return {
            "id" : self.id,
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
