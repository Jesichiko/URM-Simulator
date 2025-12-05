from abc import ABC, abstractmethod


class Instruction(ABC):
    @abstractmethod
    def exec(self, list_of_all_registers: dict, args): ...

    def __repr__(self): ...
