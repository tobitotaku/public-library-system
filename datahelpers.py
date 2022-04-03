from enum import Enum

import json;
import csv

from models import Member

TargetFile = Enum("target", "Member Book Backup")

class DataResolver:
    def Save(self, object, target : TargetFile):
        if(not isinstance(object, list)):
            object = [object]

        if(target == TargetFile.Book):
            return JSONDataLayer.WriteToFile(self, target= target, collection=object)

        if(target == TargetFile.Member):
            return CSVDataLayer.WriteToFile(self, target= target, collection=object)


    def Read(self, target : TargetFile, ReturnType):
        # if(target == TargetFile.Member):
            # return CSVDataLayer.ReadFromFile(self, target= target, objectType=ReturnType)
        if(target == TargetFile.Member):
            return JSONDataLayer.ReadFromFile(self, target= target, objectType=ReturnType)





class JSONDataLayer:
    def WriteToFile(self, target: TargetFile, collection : list()):
        jString = json.dumps([ob.__dict__ for ob in collection])
        with open('./data/' + target.name + '.json', 'w') as outfile:
            outfile.write(jString)
        print(jString)


    def ReadFromFile(self, target : TargetFile, objectType):
        ret = []
        with open('./data/' + target.name + '.json') as json_file:
            data = json.load(json_file)
            print(data)
            for row in data:
                print(row)
                ret.append(objectType(row))
        return ret


class CSVDataLayer:

    def WriteToFile(self, target : TargetFile,  collection :  list() ):
        with open( "./data/" + target.name + ".csv", mode='w') as toFile:
            writer = csv.DictWriter(toFile,fieldnames=collection[0].toHeader(),  delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for obj in collection : 
                writer.writerow(obj.toRow())


    def ReadFromFile(self, target : TargetFile, objectType) :
        ret = []        
        with open("./data/" + target.name + '.csv', newline='') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                print(row)
                ret.append(objectType(row))
        return ret