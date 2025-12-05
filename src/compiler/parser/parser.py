from typing import Literal
from src.compiler.parser.implementations.instructions import J, S, T, Z
from src.compiler.parser.interfaces.instruction import Instruction


class Parser:
    def __init__(self, tokens: list[tuple]):
        self.ast: list[tuple[str, Instruction, tuple]] = []

        # instrucciones posibles
        self.possibly_instructions: dict[str, type[Instruction]] = {
            "z": Z,
            "s": S,
            "t": T,
            "j": J,
        }

        # aridad de instrucciones
        self.expected_arity: dict[str, int] = {
            "z": 1,
            "s": 1,
            "t": 2,
            "j": 3,
        }
        self.current_token_idx = 0
        self.tokens = tokens

    def _get_token(self) -> tuple | Literal[False]:
        if self.current_token_idx < len(self.tokens):
            token = self.tokens[self.current_token_idx]
            self.current_token_idx += 1
            return token
        return False

    def _peek_token(self) -> tuple | Literal[False]:
        if self.current_token_idx < len(self.tokens):
            return self.tokens[self.current_token_idx]
        return False

    def _parse_instruction(self) -> tuple | str:
        inst_token = self._get_token()
        # inst_token[0] -> tipo del token (INSTRUCCION, NUMBER, COMMA, ...)
        # inst_token[1] -> valor del token

        # si al tratar de construir la instruccion actual esta no
        # empieza por una letra valida retornamos error
        if (
            not inst_token
            or inst_token[0] != "LETTER"
            or inst_token[1] not in self.possibly_instructions.keys()
        ):
            return f"Error: Se esperaba una instruccion valida, se encontro {inst_token} en linea "
        instruction_value = inst_token[1]

        # si no hay "(" despues del nombre de la instruccion retornamos error
        if self._get_token()[0] != "BEGIN_P":
            return f"Error: Se esperaba '(' despues de la instruccion {instruction_value} en linea "

        # Consumimos los argumentos hasta llegar a )
        args: list[int] = []
        while True:
            arg_token = self._get_token()

            if arg_token[0] != "NUMBER":
                return f"Error: Argumento invalido 'token:{arg_token}' para la instruccion {instruction_value} en linea "

            number = int(arg_token[1])  # casteamos de str a int
            if number <= 0:
                return "Error: Numero invalido como parametro en linea "
            args.append(number)

            peek = self._peek_token()
            if not peek:
                return "Error: Se esperaba resto de token"

            if peek[0] == "COMMA":
                self._get_token()  # consumir ','
                continue

            elif peek[0] == "END_P":
                self._get_token()  # consumir ')'
                break

            else:
                return f"Error: Se esperaba ',' o ')', se encontro {arg_token[1]} en linea "

        # aridad de parametros
        expected_count = self.expected_arity[instruction_value]
        actual_count = len(args)

        if actual_count != expected_count:
            return (
                f"Error: Aridad inesperada para instruccion {
                    instruction_value
                }, se esperaban {expected_count} argumentos, "
                f"pero se encontraron {actual_count} en linea "
            )

        # creamos la instruccion final
        InstClass = self.possibly_instructions[instruction_value]
        return (InstClass(), tuple(args))  # (instruccion, argumentos)

    def generate_AST(self) -> list[tuple] | str:
        line = 0

        while self.current_token_idx < len(self.tokens):
            result = self._parse_instruction()
            line += 1

            if isinstance(result, str):  # error
                return result + str(line)

            self.ast.append(result)
        return self.ast
