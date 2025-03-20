from abc import ABC, abstractmethod


class InputInterface(ABC):
    @abstractmethod
    def __init__(self, data):
        pass

    @abstractmethod
    def __call__(self, is_call):
        pass

class FactorInterface(ABC):
    @abstractmethod
    def create_factor(self, datas: dict):
        pass

