import string
from datahelpers import DataResolver, TargetFile
from ast import Pass
import json
import re
from models import Person
from multiprocessing.spawn import prepare
from utils import getNewId, getNewIdTarget
import re
import os
from os.path import exists

class UserManager:

    users = []

    def __init__(self):
        self.__resolver = DataResolver()
        self.all()

    def all(self, force = True):
        if len(self.users) == 0 or force:
            self.users = self.__resolver.Read( TargetFile.Member, Person)
        return self.users

    def findbyid(self, id):
        user = False
        self.all()
        if self.users:
            # for item in self.users:
                if id < len(self.users):
                    user = self.users[id]
        return user
    
    def findbyname(self, name):
        user = False
        self.all()
        if self.users:
            for item in self.users:
                if name.lower() == item.username.lower():
                    return item
        return user
    
    def add(self, *args):
        id = getNewIdTarget(TargetFile.Member.name)
        user = Person(id, *args)
        self.users.append(user)
        self.__resolver.Save(self.users, TargetFile.Member)
        return user    
    
    def update(self, id, user):
        self.all()
        if self.users:
            # for i,item in enumerate(self.users):
                if id < len(self.users):
                    self.users[id] = user
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return user
    
    def delete(self, id):
        self.all()
        if self.users:
            # for i,item in enumerate(self.users):
                if id < len(self.users):
                    del self.users[id]
                    self.__resolver.Save(self.users, TargetFile.Member)
                    return id

    def bulkInsert(self, filename ):
        notadded = []
        try:
            importlist = self.__resolver.csvResolver.ReadFromFileName(filename, Person)
        except:
            print('Incorrect CSV Format in importfile!')
            return notadded
        self.all()
        for i,item in enumerate(importlist):
            user = self.findbyname(item.username)
            if user:
                notadded.append(item)
            elif any(ele.isupper() for ele in item.username): 
                notadded.append(item)
            else:
                item.userid = getNewIdTarget(TargetFile.Member.name)
                self.users.append(item)
                self.__resolver.Save(self.users, TargetFile.Member)
        return notadded

    def readImportAvailable(self):
        options = []
        if not exists('./data/import/'):
            os.mkdir('./data/import/')
        for file in os.listdir("./data/import"):
            if re.search('.csv$', file, re.IGNORECASE):
                options.append(os.path.join("./data/import/", file))
        return options