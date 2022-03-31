class Member:
    csvFields = ["name"]

    def __init__ (self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age

    def toHeader(self):
        return ["name", "surname", "age"]

    def toRow(self):
        return [self.name, self.surname, self.age]



class Book:
    csvFields = ["name"]

    def __init__ (self, author, title):
        self.author = author
        self.title = title

    def toHeader(self):
        return ["author", "title"]

    def toRow(self):
        return [self.author, self.title]