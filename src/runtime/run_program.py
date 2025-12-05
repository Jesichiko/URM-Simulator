from collections import defaultdict


class Runtime:
    def __init__(self):
        self.registers = defaultdict(int)
        self.trace = []

    def _init_registers(self, registers_input: list[int]):
        for register, value in enumerate(registers_input):
            self.registers[register] = value

    def _format_registers(self, max_display=10):
        """Formatea los registros para mostrar en la traza"""
        reg_str = []
        for i in range(max_display):
            val = self.registers[i]
            if val != 0:
                reg_str.append(f"R{i}={val}")
        return " | ".join(reg_str) if reg_str else "Todos en 0"

    def execute_program(
        self, AST: list[tuple], init_registers: list[int], max_steps: int
    ) -> int | tuple[int, int]:
        self._init_registers(registers_input=init_registers)
        current_index_instruction = 0
        steps = 0

        # Traza inicial
        self.trace.append("=== INICIO DE EJECUCION ===")
        self.trace.append(f"Registros iniciales: {self._format_registers()}")
        self.trace.append("")

        # mientras la instruccion este entre [0, ultima_instruccion]
        while current_index_instruction < len(AST):
            current_instruction, args = AST[current_index_instruction]
            steps += 1

            # formato de la instruccion para la traza
            inst_name = current_instruction.__repr__()
            args_str = ", ".join(map(str, args))

            # registramos antes de ejecutar
            self.trace.append(
                f"Paso {steps}: Linea {current_index_instruction + 1} -> {inst_name}({
                    args_str
                })"
            )

            if steps >= max_steps:
                self.trace.append("")
                self.trace.append("*** LIMITE DE ITERACIONES ALCANZADO ***")
                self.trace.append(f"Registros finales: {
                                  self._format_registers()}")
                return self.registers[0], self.trace, steps

            # ejecutamos la funcion del indice actual
            possibly_jump = current_instruction.exec(self.registers, args)

            # mostramos traza de la funcion actual
            if inst_name == "Z":
                self.trace.append(f"  -> R{args[0]} = 0")
            elif inst_name == "S":
                self.trace.append(
                    f"  -> R{args[0]} = {self.registers[args[0]]}")
            elif inst_name == "T":
                self.trace.append(
                    f"  -> R{args[1]} = R{args[0]} = {self.registers[args[1]]}"
                )
            elif inst_name == "J":
                if possibly_jump:
                    register1_val = self.registers[args[0]]
                    register2_val = self.registers[args[1]]
                
                    self.trace.append(
                            f"  -> R{args[0]}({register1_val}) == R{args[1]}({
                                register2_val
                            }): SALTAR a linea {possibly_jump}"
                        )
                    # convertimos el indice al indice de la lista
                    current_index_instruction = (
                        possibly_jump - 1
                    )  # convertir de base 1 a base 0
                    self.trace.append("")
                    continue

                else:
                    r1_val = self.registers[args[0]]
                    r2_val = self.registers[args[1]]
                    self.trace.append(
                        f"  -> R{args[0]}({r1_val}) != R{args[1]}({r2_val}): Continuar"
                    )

            # estado de registros despues de cada paso
            self.trace.append(f"  Estado: {self._format_registers()}")
            self.trace.append("")

            # cualquier otra funcion
            current_index_instruction += 1

        # fin exitoso
        self.trace.append("=== EJECUCION COMPLETADA ===")
        self.trace.append(f"Resultado en R0: {self.registers[0]}")
        self.trace.append(f"Total de pasos: {steps}")

        return self.registers[0], self.trace, steps
