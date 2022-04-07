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

    def all(self):
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
    
    def add(self):
        self.__resolver.Save(self.__resolver, self.users, TargetFile.Member)
    
    def update(self):
        pass
