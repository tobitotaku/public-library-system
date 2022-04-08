from datahelpers import DataResolver, TargetFile
from ast import Pass
import json
from models import Person
from multiprocessing.spawn import prepare



class UserManager:

    users = []

    def __init__(self):
        self.__resolver = DataResolver()
        self.all()

    def all(self, force = False):
        if len(self.users) == 0 or force:
            self.users = self.__resolver.Read( TargetFile.Member, Person)
        return self.users

    def findbyname(self, username):
        user = False
        self.all()
        if self.users:
            for item in self.users:
                if item.username == username:
                    return item
        return user
    
    def add(self, user):
        self.users.append(user)
        self.__resolver.Save(self.users, TargetFile.Member)
        return user
    
    def update(self, username, user):
        self.all()
        if self.users:
            for i,item in enumerate(self.users):
                if item.username == username:
                    self.users[i] = user
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return user
    
    def delete(self, username):
        self.all()
        if self.users:
            for i,item in enumerate(self.users):
                if item.username == username:
                    del self.users[i]
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return username
