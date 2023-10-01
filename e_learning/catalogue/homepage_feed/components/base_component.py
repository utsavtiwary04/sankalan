from abc import ABC, abstractmethod

class BaseComponent(ABC):

    @abstractmethod
    def validate(self):
        pass
