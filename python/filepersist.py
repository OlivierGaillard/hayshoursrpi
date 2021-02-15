import os
from os import path
from persist import Persistable


class FilePersist(Persistable):
    """
    Save / retrieve the last hour using a file.
    """

    def __init__(self, rootdir, filename):
        self.stateful_type = "File"
        self.rootdir = rootdir
        self.fname = path.join(rootdir, filename)
        self.fdb = None
        self.initStorage(self.fname)

    def get_stateful_type(self):
        return self.stateful_type

    def initStorage(self, storage_name):
        if not path.exists(self.rootdir):
            os.mkdir(self.rootdir)
        if not path.exists(self.fname):
            self.fdb = open(self.fname, "w+")
        else:
            self.fdb = open(self.fname, "a+")

    def save(self, result):
        if self.fdb.closed:
            self.fdb = open(self.fname, "a+")
        self.fdb.write(result + "\n")
        self.fdb.close()

    def readLast(self):
        self.fdb.close()
        self.fdb = open(self.fname, "r")
        lines = self.fdb.readlines()
        self.fdb.close()
        count = len(lines)
        if count > 0:
            lastLine = len(lines) - 1
            lastItem = lines[lastLine]
            lastItem = lastItem.replace('\n','')
            return lastItem
        else:
            return ""

    def deleteStorage(self):
        if path.exists(self.fname):
            os.remove(self.fname)
