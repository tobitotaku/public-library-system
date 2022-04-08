
import operator

def getNewId(inputList) :
    return int(max(inputList, key=operator.attrgetter("id")).id) + 1

