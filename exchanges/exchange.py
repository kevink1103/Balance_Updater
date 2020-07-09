from abc import ABCMeta, abstractmethod

class Exchange(metaclass=ABCMeta):

    @abstractmethod
    def get_balance(self):
        pass
    
    @abstractmethod
    def get_orderbook(self):
        pass
