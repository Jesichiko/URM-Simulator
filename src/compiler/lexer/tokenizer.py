class Tokenizer:
    def __init__(self):
        self.program: list[str] = None
        self.token_types = {"(": "BEGIN_P", ")": "END_P", ",": "COMMA"}

    """
    Dada una entrada del tipo:
    - input: list[str]
    retornaremos:
    - output: list[str]
    preprocesada, esto es, sin espacios, sin mayusculas y sin lineas vacias
    """

    def load_program(self, input: list[str]) -> list[str]:
        self.program = [line.strip().lower() for line in input if line.strip().lower()]

    def load_from_file(self, filename: str) -> list[str]:
        with open(filename, "r") as file:
            self.program = [
                line.strip().lower() for line in file if line.strip().lower()
            ]

    """
    Tokenizamos el programa cargado (si es que lo esta)
    y retornamos una lista de tuplas del tipo:
     [(tipo, valor), (tipo, valor), (tipo, valor) ...]
    """

    def tokenize_program(self) -> list[tuple]:
        tokenized_program = []
        if not self.program:
            return None

        for line in self.program:
            char_idx = 0

            while char_idx < len(line):
                char = line[char_idx]

                # separadores de instrucciones
                if char in self.token_types:
                    tokenized_program.append((self.token_types[char], char))
                    char_idx += 1
                    continue

                # letras
                if char.isalpha():
                    start_idx = char_idx
                    while char_idx < len(line) and line[char_idx].isalpha():
                        char_idx += 1
                    tokenized_program.append(
                        ("LETTER", line[start_idx:char_idx].lower())
                    )

                # digitos
                elif char.isdigit():
                    start_idx = char_idx
                    while char_idx < len(line) and line[char_idx].isdigit():
                        char_idx += 1
                    tokenized_program.append(("NUMBER", line[start_idx:char_idx]))
                else:
                    char_idx += 1
        return tokenized_program
