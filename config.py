# from enum import Enum
# import os;
import configparser

class configurationhelper:

    def __init__(self):
        self.parser = configparser.RawConfigParser() 
        self.parser.read("./config.txt")

    def getMembersFile(self):
        return "./" + self.parser.get("memberDataFileName")

    def getBooksFile(self):
        return "./" + self.parser.get("booksDataFile")