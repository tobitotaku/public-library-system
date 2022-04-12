import string
from datahelpers import DataResolver, TargetFile
from ast import Pass
import json
from models import Person
from multiprocessing.spawn import prepare
from utils import getNewId

class UserManager:

    users = []

    def __init__(self):
        self.__resolver = DataResolver()
        self.all()

    def all(self, force = False):
        if len(self.users) == 0 or force:
            self.users = self.__resolver.Read( TargetFile.Member, Person)
        return self.users

    def findbyid(self, id):
        user = False
        self.all()
        if self.users:
            for item in self.users:
                if item.id == id:
                    return item
        return user
    
    def findbyname(self, username):
        user = False
        self.all()
        if self.users:
            for item in self.users:
                if item.username == username:
                    return item
        return user
    
    def add(self, *args):
        id = getNewId(self.users)
        user = Person(id, *args)
        self.users.append(user)
        self.__resolver.Save(self.users, TargetFile.Member)
        return user    
    
    def update(self, id, user):
        self.all()
        if self.users:
            for i,item in enumerate(self.users):
                if item.id == id:
                    self.users[i] = user
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return user
    
    def delete(self, id):
        self.all()
        if self.users:
            for i,item in enumerate(self.users):
                if item.id == id:
                    del self.users[i]
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return id

    def bulkInsert(self, filename ):
        data = self.all()
        data.extend(self.__resolver.csvResolver.ReadFromFileName(filename, Person))
        self.__resolver.Save(data, TargetFile.Member)