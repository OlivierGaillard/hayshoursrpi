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

    @abstractmethod
    def get_stateful_type(self):
        pass
