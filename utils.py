
import operator

def getNewId(inputList) :
    if len(inputList) == 0:
        return 0
    return int(max(inputList, key=operator.attrgetter("id")).id) + 1

