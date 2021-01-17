import os
from os import path
from abc import ABC, abstractmethod


class Persistable(ABC):

    @abstractmethod
    def save(self, result):
        pass

    @abstractmethod
    def readLast(self):
        pass

    @abstractmethod
    def initStorage(self, storage_name):
        pass

    @abstractmethod
    def deleteStorage(self):
        pass


class FilePersist(Persistable):
    """
    Save / retrieve the last hour using a file.
    """

    def __init__(self, filename):
        self.fname = filename
        self.fdb = None
        self.initStorage(self.fname)

    def initStorage(self, storage_name):
        if not path.exists(self.fname):
            self.fdb = open(self.fname, 'w+')
        else:
            self.fdb = open(self.fname, 'a+')

    def save(self, result):
        self.fdb.write(result+'\n')
        self.fdb.close()

    def readLast(self):
        self.fdb.close()
        self.fdb = open(self.fname, 'r')
        lines = self.fdb.readlines()
        self.fdb.close()
        count = len(lines)
        if count > 0:
            lastLine = len(lines) - 1
            lastItem = lines[lastLine]
            return lastItem
        else:
            return ''

    def deleteStorage(self):
        if path.exists(self.fname):
            os.remove(self.fname)
