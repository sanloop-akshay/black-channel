from abc import ABC, abstractmethod

class IAction(ABC):
    """Abstract action interface for buttons."""

    @abstractmethod
    def execute(self):
        pass
