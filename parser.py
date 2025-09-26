from lexer import tokenize, read_file, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, type_=None, value=None):
        tok = self.current()
        if not tok:
            return None
        if type_ and tok.type != type_:
            raise SyntaxError(f"Expected type {type_}, got {tok.type}")
        if value and tok.value != value:
            raise SyntaxError(f"Expected value {value}, got {tok.value}")
        self.pos += 1
        return tok

    def parse(self):
        ir = {
            "qubits": 0,
            "gates": [],
            "measurements": [],
            "shots": 1024,
            "macros": {}
        }

        while self.current():
            tok = self.current()

            if tok.type == "KEYWORD":
                if tok.value == "QUBIT":
                    self.eat("KEYWORD")
                    num = self.eat("NUMBER")
                    ir["qubits"] = num.value

                elif tok.value in ("H", "X"):
                    gate = self.eat("KEYWORD")
                    target = self.eat("NUMBER")
                    ir["gates"].append((gate.value, target.value))

                elif tok.value == "CNOT":
                    self.eat("KEYWORD")
                    control = self.eat("NUMBER")
                    target = self.eat("NUMBER")
                    ir["gates"].append(("CNOT", control.value, target.value))

                elif tok.value == "MEASURE":
                    self.eat("KEYWORD")
                    target = self.eat("NUMBER")
                    ir["measurements"].append(target.value)

                elif tok.value == "RUN":
                    self.eat("KEYWORD")
                    shots = self.eat("NUMBER")
                    ir["shots"] = shots.value

                elif tok.value == "DEF":
                    self.eat("KEYWORD")
                    name = self.eat("IDENTIFIER").value
                    self.eat("EQUALS")
                    macro_cmds = []
                    while self.current() and not (self.current().type == "SEMICOLON"):
                        macro_cmds.append(self.eat().value)
                    self.eat("SEMICOLON")
                    ir["macros"][name] = macro_cmds

                else:
                    raise SyntaxError(f"Unknown keyword {tok.value}")

            else:
                self.eat()  # skip any unexpected token

        return ir

