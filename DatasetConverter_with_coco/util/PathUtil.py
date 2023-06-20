from os.path import exists


def fixPath(path):
    return path.replace('\\', '/')


def changeExt(path, newExt):
    oldExt = path.split(".")[-1]
    return path.replace(f".{oldExt}", f".{newExt}")


def findByExtList(path, extList):
    for ext in extList:
        test = changeExt(path, ext)
        if exists(test):
            return test


def extractExt(path):
    return path.split(".")[-1]


def changeTargetFile(path, target):
    oldFile = path.split("/")[-1]
    return path[0:len(path) - len(oldFile)] + target
