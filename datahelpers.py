from enum import Enum
from fileinput import filename
import os.path
import os
from os.path import exists
# from pathlib import Path
from ast import literal_eval

import string
import time
import datetime
import json;
import csv
from utils import *
from numpy import integer

from models import LoanItem, Person, Book, BookItem
# from usermodels import Person

TargetFile = Enum("target", "Member Book Backup LibraryItem LoanItem")

class DataResolver:
    def __init__(self):
        self.jsonResolver : JSONDataLayer = JSONDataLayer()
        self.csvResolver : CSVDataLayer = CSVDataLayer()

        return

    def Save(self, object, target : TargetFile):
        if(not isinstance(object, list) & (target != TargetFile.Backup)):
            object = [object]

        if(target == TargetFile.Book):
            return self.jsonResolver.WriteToFile( target= target, collection=object)

        if(target == TargetFile.Member):
            return self.jsonResolver.WriteToFile( target= target, collection=object)

        if(target == TargetFile.Backup):
            return self.jsonResolver.WriteBackupToFile( collection=object)
        if(target == TargetFile.LibraryItem):
            return self.jsonResolver.WriteToFile( target= target, collection=object)
        if(target == TargetFile.LoanItem):
            return self.jsonResolver.WriteToFile( target= target, collection=object)

    def Read(self, target : TargetFile, ReturnType):
        if(target == TargetFile.Book):
            return self.jsonResolver.ReadFromFile( target= target, objectType=ReturnType)
        if(target == TargetFile.Member):
            return self.jsonResolver.ReadFromFile( target= target, objectType=ReturnType)
        if(target == TargetFile.LibraryItem):
            return self.jsonResolver.ReadFromFile( target= target, objectType=ReturnType)
        if(target == TargetFile.LoanItem):
            return self.jsonResolver.ReadFromFile( target= target, objectType=ReturnType)
        # if(target == TargetFile.Backup):
            # return self.jsonResolver.ReadBackup( target= target, objectType=ReturnType)

    def ReadBackup(self, file):
        return self.jsonResolver.ReadBackup(file)



class JSONDataLayer:

    def __init__(self):
        return

    #got to love some recursive functions <3
    def findFileName(self, name : string, extension : string, number : integer) -> string:
        file = name + '_'+ str(number)+str(extension)
        if os.path.exists(file):
            return self.findFileName(name, extension, number+1)
        else:
            return str(file)


    def WriteBackupToFile(self, collection):
        ct =  datetime.datetime.now().strftime("%d-%m-%Y")
        filename = self.findFileName('./data/backups/backup_' + ct, '.json', 0)
        jString = json.dumps(collection, indent=4)


        with open(filename, 'w') as outfile:
            outfile.write(jString)



    def ReadBackup(self, filename):
        if not exists(filename):
            print("Please enter a file that exists.")
            return [], []
        members_ret = []
        books_ret = []
        booksItems_ret = []
        loanItems_ret = []
        with open(filename, 'r') as json_file:
            try:
                input = json_file.read()
                data = json.loads(input)

                for row in data[0]['members']:
                    members_ret.append(Person(row))
                
                for row in data[0]['books']:
                    books_ret.append(Book(row))

                for row in data[0]['libraryItems']:
                    booksItems_ret.append(BookItem(row))

                for row in data[0]['loanitems']:
                    loanItems_ret.append(LoanItem(row))

            except Exception as e: print("Something went wrong with loading backup, please check if all files are setup correcty or contact the system administrator: " + e)
              



        # print([b.userId for b in loanItems_ret])
        # print([b.username for b in members_ret])
        return  members_ret, books_ret, booksItems_ret, loanItems_ret
        

        

    def WriteToFile(self, target: TargetFile, collection : list()):
        toStore = [ob.toRow() for ob in collection]
        jString = json.dumps(toStore, indent=4)#.replace(' ', '').replace('\n', '')
        # jString = json.dumps(collection)
        with open('./data/' + target.name + '.json', 'w') as outfile:
            try:
                outfile.write(jString)
            except:
                return False
            


    def ReadFromFile(self, target : TargetFile, objectType):
        if not exists('./data/' + target.name + '.json'):
            with open('./data/' + target.name + '.json', 'w') as outfile: 
                outfile.write('[]')

        ret = []
        with open('./data/' + target.name + '.json') as json_file:
            try:
                data = json.load(json_file)
                for row in data:
                    ret.append(objectType(row))
            except:
                print("Something went wrong with loading " + target.name + ".json, please check if all files are setup correcty or contact the system administrator")
        return ret

    def ReadFromFileName(self, targetfile, objectType) :
        ret = []        
        with open(targetfile, newline='') as f:
            reader = json.load(f)
            for row in reader:
                ret.append(objectType(row))
        return ret


        
class CSVDataLayer:

    def __init__(self):
        return


    def WriteToFile(self, target : TargetFile,  collection :  list() ):
        with open( "./data/" + target.name + ".csv", mode='w') as toFile:
            writer = csv.DictWriter(toFile,fieldnames=collection[0].toHeader(),  delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for obj in collection : 
                writer.writerow(obj.toRow())


    def ReadFromFile(self, target, objectType) :
        if not exists('./data/' + target.name + '.json'):
            with open('./data/' + target.name + '.json', 'w'): pass

        ret = []        
        with open("./data/" + target.name + '.csv', newline='') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                ret.append(objectType(row))
        return ret

    def ReadFromFileName(self, targetfile, objectType) :
        if not exists(targetfile):
            with open(targetfile, 'w'): pass
        ret = []        
        with open(targetfile, newline='') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                ret.append(objectType(row))
        return ret