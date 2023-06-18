from abc import ABC, abstractmethod

class ManagerInterface(ABC):
    def __init__(self):
        print("Init")
    @abstractmethod
    def create(self, data):
        print("Parent method")

    def retrieve(self, data):
        print("Common method")

    def update(self, data):
        print("Common method")