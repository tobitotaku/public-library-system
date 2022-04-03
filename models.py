import json
class Member:

    # def __init__ (self, name, surname, age):
    #     self.name = name
    #     self.surname = surname
    #     self.age = age


    def __init__(self, *args):
        # print("inside Member: " )
        # print(args)
        if len(args) > 2:
            self.name = args[0]
            self.surname = args[1]
            self.age = args[2]

        else:
            self.name = args[0]['name']
            self.surname = args[0]['surname']
            self.age = args[0]['age']


    def toHeader(self):
        return ["name", "surname", "age"]

    def toRow(self):
        return {"name" : self.name, "surname" : self.surname, "age" : self.age}





class Book:

    def __init__ (self, ID, Author, Title, ISBN):
        self.author = Author
        self.title = Title
        self.ID = ID
        self.ISBN = ISBN

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



