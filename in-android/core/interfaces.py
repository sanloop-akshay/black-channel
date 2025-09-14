from abc import ABC, abstractmethod

class IAction(ABC):

    @abstractmethod
    def execute(self):
        pass
