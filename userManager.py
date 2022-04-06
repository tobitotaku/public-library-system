from datahelpers import DataResolver, TargetFile
from ast import Pass
import json
from models import Person
from multiprocessing.spawn import prepare



class UserManager:

    users = []

    def __init__(self):
        self.__resolver = DataResolver()
        self.users = self.__resolver.Read(TargetFile.Member, Person )
        # @staticmethod

    def all(self):
        list = self.__resolver.Read( TargetFile.Member, Person)
        return list

    def findbyname(self, username):
        user = False
        list = self.all()
        if list:
            for item in list:
                if item.username == username:
                    return item
        return user
    
    def add(self):
        list_users = self.all()
        self.__resolver.Save(self.__resolver, list_users, TargetFile.Member)
