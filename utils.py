
import operator

def getNewId(inputList) :
    if len(inputList) == 0:
        return 1
    return int(max(inputList, key=operator.attrgetter("id")).id) + 1

def s(a, b = 20):
    return str(a) + ' '*(b-len(str(a)))