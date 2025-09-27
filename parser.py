from lexer import tokenize, read_file, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.macros = {}

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
            "shots": 1024
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
                    # Macro invocation or execution shots
                    if self.current() and self.current().type == "IDENTIFIER":
                        name = self.eat("IDENTIFIER").value
                        args = []
                        while self.current() and self.current().type == "NUMBER":
                            args.append(self.eat("NUMBER").value)
                        if name not in self.macros:
                            raise SyntaxError(f"Undefined macro {name}")
                        expanded = self.expand_macro(name, args)
                        ir["gates"].extend(expanded)
                    else:
                        shots = self.eat("NUMBER")
                        ir["shots"] = shots.value

                elif tok.value == "DEF":
                    self.eat("KEYWORD")
                    name = self.eat("IDENTIFIER").value
                    params = []
                    while self.current() and self.current().type == "IDENTIFIER":
                        params.append(self.eat("IDENTIFIER").value)
                    self.eat("SEMICOLON")

                    body = []
                    while self.current() and not (self.current().type == "KEYWORD" and self.current().value == "END"):
                        body.append(self.eat())
                    self.eat("KEYWORD", "END")

                    self.macros[name] = (params, body)

                else:
                    raise SyntaxError(f"Unknown keyword {tok.value}")

            else:
                self.eat()  # skip unexpected token

        return ir

    def expand_macro(self, name, args):
        params, body = self.macros[name]
        if len(params) != len(args):
            raise SyntaxError(f"Macro {name} expects {len(params)} args, got {len(args)}")

        subst = {p: a for p, a in zip(params, args)}
        expanded = []

        i = 0
        while i < len(body):
            tok = body[i]
            if tok.type == "KEYWORD" and tok.value in ("H", "X"):
                gate = tok.value
                i += 1
                target = body[i].value if body[i].type == "NUMBER" else subst.get(body[i].value)
                expanded.append((gate, int(target)))
            elif tok.type == "KEYWORD" and tok.value == "CNOT":
                i += 1
                c = body[i].value if body[i].type == "NUMBER" else subst.get(body[i].value)
                i += 1
                t = body[i].value if body[i].type == "NUMBER" else subst.get(body[i].value)
                expanded.append(("CNOT", int(c), int(t)))
            i += 1
        return expanded
