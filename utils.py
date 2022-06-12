
import operator
from models import LastIds
from datahelpers import DataResolver, TargetFile

def getNewId(inputList) :
    if len(inputList) == 0:
        return 1
    return int(max(inputList, key=operator.attrgetter("id")).id) + 1

def getNewIdTarget(Target):
    resolver = DataResolver()
    all = resolver.Read( TargetFile.LastIds, LastIds)
    for i,obj  in enumerate(all):
        if Target == obj.file:
            all[i].maxid += 1
            resolver.Save(all, TargetFile.LastIds)
            return obj.maxid
    lastIdObj = LastIds(Target, 0)
    all.append(lastIdObj)
    resolver.Save(all, TargetFile.LastIds)
    return getNewIdTarget(Target)

def s(a, b = 20):
    return str(a) + ' '*(b-len(str(a)))