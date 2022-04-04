

from datahelpers import DataResolver, JSONDataLayer, TargetFile

class Person:
    def __init__(self, *args):
        self.role = 'member'
        if len(args) > 2:
            self.username = args[0]
            self.surname = args[1]
            self.age = args[2]
            self.password = args[3]
            if 4 in args:
                self.role = args[4]
        else:
            self.username = args[0]['username']
            self.surname = args[0]['surname']
            self.age = args[0]['age']
            self.password = args[0]['password']
            self.role = args[0]['role']

    def toHeader(self):
        return ["username", "surname", "age", "password", "role", "id"]

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
    def allmembers():
        list = Person.all()
        check_admin = lambda o: o.role == 'admin'
        filter(check_admin, list)
        return list

    @staticmethod
    def findbyname(username, list = False):
        user = False
        if not list:
            list = Person.all()
        if list:
            for item in list:
                if item.username == username:
                    return item
        return user
    
    def add(self):
        resolver = DataResolver()
        list = Person.all()
        user = Person.findbyname(self.username, list)
        if not user:
            list.append(self)
            DataResolver.Save(resolver, list, TargetFile.Member)
            messagestr = 'member added'
        return self

    def update(self):
        resolver = DataResolver()
        list = Person.all()
        user = Person.findbyname(self.username, list)
        if not user:
            list.append(self)
            DataResolver.Save(resolver, list, TargetFile.Member)
            messagestr = 'member added'
        return self
    # def validate(self, username):
    #     user = self.findbyname(username)
    #     return user

class Member(Person):
    pass
    
class LibraryAdmin(Person):
    def __init__ (self, *args):
        Person.__init__(self, *args)
        self.role = 'admin'
