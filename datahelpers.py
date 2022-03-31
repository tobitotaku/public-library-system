# from array import list
# from array import 
from enum import Enum
from operator import attrgetter

# this file is for the parser to and from csv and json
import json;
import csv

from config import configparser
from models import Member

TargetFile = Enum("target", "Member Book Backup")
# read csv files and convert to objects
# read json files and convert to objects

# convert object to csvs
# convert json to csv

#read jsons

class DataResolver:
    def save(self, object, target : TargetFile):
        if(not isinstance(object, list)):
            object = [object]

        if(target == TargetFile.Book):
            return CSVDataLayer.WriteToFile(self, target= target, collection=object)

        if(target == TargetFile.Member):
            return CSVDataLayer.WriteToFile(self, target= target, collection=object)


class JSONDataLayer:

    def WriteToFile(self, item):
        jString = json.dumps(item.__dict__)
        print(jString)

class CSVDataLayer:


    def WriteToFile(self, target : TargetFile,  collection :  list() ):
        print("writing to: " + target.name)
        with open( "./data/" + target.name + ".csv", mode='w') as toFile:
            writer = csv.writer(toFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(collection[0].toHeader())

            for obj in collection : 
                writer.writerow(obj.toRow())
