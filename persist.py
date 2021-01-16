from os import path


class FilePersist(object):
    """
    Save / retrieve the last hour.
    """

    def __init__(self, dbname):
        self.fname = dbname

    def save(self, result):
        if not path.exists(self.fname):
            f = open(self.fname, 'w+')
            f.write(result)
            f.write('\n')
            f.close()
        else:
            f = open(self.fname, 'a+')
            f.write(result)
            f.write('\n')
            f.close()

    def readLast(self):
        if path.exists(self.fname):
            f = open(self.fname, 'r')
            lines = f.readlines()
            lastLine = len(lines) - 1
            lastItem = lines[lastLine]
            f.close()
            return lastItem
        else:
            return ''
