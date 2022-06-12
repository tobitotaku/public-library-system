import json
from enum import Enum
from ast import Pass
import json
# import datetime
from datetime import datetime, date
from multiprocessing.spawn import prepare

# itemType = Enum("itemType", "book magazine")
itemStatus = Enum("itemStatus", "available loaned")

class LastIds:
        def __init__(self, *args):
            if len(args) > 1:
                self.file = args[0]
                self.maxid = args[1]
            else:
                self.file = args[0]['file']
                self.maxid = args[0]['maxid']
        def getId(self):
            return self.file

        def toHeader(self):
            return ["file","maxid"]

        def toRow(self):
            return { "file" : self.file, "maxid" : self.maxid}

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=0)
class Book:

    def __init__(self, *args):
        if len(args) > 2:
            self.id = args[0]
            self.bookid = self.id
            self.author = args[1]
            self.title = args[2]
            self.ISBN = args[3]

        else:
            self.id = args[0]['id']
            self.bookid = self.id
            self.author = args[0]['author']
            self.title = args[0]['title']
            self.ISBN = args[0]['ISBN']

    def getId(self):
        return self.bookid

    def toHeader(self):
        return ["id","bookid","author", "title",  "ISBN"]

    def toRow(self):
        return { "id" : self.id,"bookid" : self.bookid, "author" : self.author, "title" : self.title, "ISBN" : self.ISBN}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)


class BookItem(Book):

    def __init__(self, *args):
        if len(args) > 1:
            Book.__init__(self, args[2].__dict__)
            self.id = args[0]
            self.bookItemId = self.id
            # self.bookid = args[5]
            self.itemStatus = args[1] if len(args) > 1 and args[1] is not None else itemStatus.available.name

        else:
            Book.__init__(self, *args)
            self.id = args[0]['id']
            self.bookItemId = args[0]['bookItemId']
            # self.bookid = args[0]['bookid']
            self.itemStatus = args[0]['itemStatus']
    
    def getId(self):
        return self.bookItemId

    def toHeader(self):
        return ["id","bookItemId","bookid", "itemStatus","author", "title",  "ISBN"]

    def toRow(self):
        return {"id" : self.id, "bookItemId" : self.bookItemId, "bookid" : self.bookid, "itemStatus" : self.itemStatus, "author" : self.author, "title" : self.title, "ISBN" : self.ISBN}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)

class Person:
    def __init__(self, *args):
        if len (args) == 0:
            return
        if len(args) > 3:
            self.id = args[0]
            self.userid = self.id
            self.username = args[1]
            self.surname = args[2]
            self.age = args[3]
            self.password = args[4]
            self.role = args[5] if 5 in args else 'member'
        else:
            self.id = args[0]['id']
            self.userid = self.id
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
            self.role = args[0]['role'] if args[0]['role'] else 'member'

    def getId(self):
        return self.id

    def toHeader(self):
        return ["id", "userid", "username", "surname", "age", "password", "role"]

    def toRow(self):
        return {
            "id" : self.id,
            "userid" : self.userid,
            "username" : self.username,
            "surname" : self.surname,
            "age" : self.age,
            "password": self.password,
            "role": self.role,
        }

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)



    # def validate(self, username):
    #     user = self.findbyname(username)
    #     return user

class Member(Person):
    Pass
    
class LibraryAdmin(Person):
    def __init__ (self, *args):
        Person.__init__(self, *args)
        self.role = 'admin'

class LoanItem(BookItem, Person):
    def __init__(self, *args):
        if len(args) > 2:
            self.id = args[0]
            self.loanItemid = self.id
            # self.bookItemId = args[1]
            # self.userId = args[1]
            self.issueDate = args[1]
            self.returnDate = args[2]
            self.loanStatus = args[3]
            BookItem.__init__(self, args[4].__dict__)
            Person.__init__(self, args[5].__dict__)

        else:
            BookItem.__init__(self, *args)
            Person.__init__(self, *args)
            self.id = args[0]['id']
            self.loanItemid = args[0]['loanItemid']
            # self.bookItemId = args[0]['bookItemId']
            # self.userId = args[0]['userId']
            self.issueDate = datetime.strptime(args[0]['issueDate'], "%d-%m-%Y")
            self.returnDate = datetime.strptime(args[0]['returnDate'], "%d-%m-%Y")
            self.loanStatus = itemStatus.loaned.name

    def getId(self):
        return self.id

    def toHeader(self):
        return ["id", "loanItemid", "bookItemId", "userId", "issueDate", "returnDate", "loanStatus"]

    def toRow(self):
        # dateObject = date.today()
        # today = date.strftime(date.today(),"%d-%m-%Y")
        # return { "id" : self.id, "bookItemId" : self.bookItemId, "userId" : self.userId, "issueDate" : self.issueDate, "returnDate" : self.returnDate, "loanStatus" : self.loanStatus}
        today = date.strftime(self.issueDate,"%d-%m-%Y")
        returnDate =  date.strftime(self.returnDate,"%d-%m-%Y")
        return { "id" : self.id, "loanItemid" : self.loanItemid, "bookItemId" : self.bookItemId, "userId" : self.userId, "issueDate" : today, "returnDate" : returnDate, "loanStatus" : self.loanStatus}

    def toJSON(self):

        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)

    
        

