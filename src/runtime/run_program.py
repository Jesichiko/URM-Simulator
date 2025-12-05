from typing import defaultdict


class Runtime:
    def __init__(self):
        self.registers = defaultdict(int)

    def _init_registers(self, registers_input: list[int]):
        for register, value in enumerate(registers_input):
            self.registers[register] = value

    def execute_program(
        self, AST: list[tuple], init_registers: list[int], max_steps: int
    ) -> int | tuple[int, int]:
        self._init_registers(registers_input=init_registers)
        current_index_instruction = 0
        steps = 0

        # mientras la instruccion este entre [0, ultima_instruccion]
        while 0 <= current_index_instruction < len(AST):
            current_instruction, args = AST[current_index_instruction]
            steps += 1

            if steps >= max_steps:
                return self.registers[0], steps

            # ejecutamos la funcion del indice actual
            possibly_jump = current_instruction.exec(self.registers, args)

            # si la funcion actual es J y la condicion fue exitosa se salta a la nueva instruccion
            if current_instruction.__repr__() == "J" and possibly_jump is True:
                jump_to_index = args[2]
                current_index_instruction = jump_to_index
                continue

            # cualquier otra funcion
            current_index_instruction += 1

        return self.registers[0], None
