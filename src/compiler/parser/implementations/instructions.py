from src.compiler.parser.interfaces.instruction import Instruction


class Z(Instruction):
    def exec(self, list_of_all_registers: dict, args: tuple):
        (register,) = args
        list_of_all_registers[register] = 0

    def __repr__(self):
        return "Z"


class S(Instruction):
    def exec(self, list_of_all_registers: dict, args):
        (register,) = args
        list_of_all_registers[register] += 1

    def __repr__(self):
        return "S"


class T(Instruction):
    def exec(self, list_of_all_registers: dict, args):
        register1, register2 = args
        list_of_all_registers[register2] = list_of_all_registers[register1]

    def __repr__(self):
        return "T"


class J(Instruction):
    def exec(self, list_of_all_registers: dict, args):
        register1, register2 = args
        if list_of_all_registers[register1] == list_of_all_registers[register2]:
            return True
        return False

    def __repr__(self):
        return "J"
