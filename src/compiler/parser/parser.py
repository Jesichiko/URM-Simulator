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
            return f"Error: Se esperaba una instruccion valida, se encontro {
                inst_token
            } en linea"

        inst_name = inst_token[1]
        if self._get_token()[0] != "BEGIN_P":
            return (
                f"Error: Se esperaba '(' despues de la instruccion {inst_name} en linea"
            )

        # Consumimos los argumentos hasta llegar a )
        args: list[int] = []
        while True:
            arg_token = self._get_token()
            if arg_token[0] != "NUMBER":
                return f"Error: Argumento invalido '{arg_token}' para la instruccion {inst_name} en linea"

            number = int(arg_token[1])  # casteamos de str a int
            if number < 0:
                return f"Error: Numero negativo invalido '{arg_token} en linea"
            args.append(number)

            peek = self._peek_token()
            if not peek:
                return "Error: Se esperaba resto de linea"

            if peek[0] == "COMMA":
                self._get_token()  # consumir ','
                continue
            elif peek[0] == "END_P":
                self._get_token()  # consumir ')'
                break
            else:
                return f"Error: Se esperaba ',' o ')' despues del argumento {arg_token[1]} en linea"

        # aridad de parametros
        expected_count = self.expected_arity[inst_name]
        actual_count = len(args)
        if actual_count != expected_count:
            return (
                f"Error: Aridad inesperada para instruccion '{
                    inst_name.upper()
                }', se esperaban {expected_count} argumentos, "
                f"pero se encontraron {actual_count} en linea"
            )

        # creamos la instruccion final
        InstClass = self.possibly_instructions[inst_name]
        return (InstClass(), tuple(args))  # (instruccion, argumentos)

    def generate_AST(self) -> list[tuple] | str:
        while self.current_token_idx < len(self.tokens):
            result = self._parse_instruction()

            if isinstance(result, str):  # error
                return result + str(self.current_token_idx)

            self.ast.append(result)
        return self.ast
