import re

TOKEN_PATTERNS = [
    (r'\s+', None),
    (r'QUBIT|DEF|END|H|X|CNOT|MEASURE|RUN', 'KEYWORD'),  # Added END
    (r'[A-Za-z_][A-Za-z0-9_]*', 'IDENTIFIER'),
    (r'[0-9]+', 'NUMBER'),
    (r'=', 'EQUALS'),
    (r';', 'SEMICOLON'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
]

TOKEN_REGEX = [(re.compile(pat), tag) for pat, tag in TOKEN_PATTERNS]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(source):
    tokens = []
    pos = 0
    while pos < len(source):
        match = None
        for regex, tag in TOKEN_REGEX:
            m = regex.match(source, pos)
            if m:
                text = m.group(0)
                if tag:
                    tokens.append(Token(tag, text if tag != "NUMBER" else int(text)))
                pos = m.end()
                match = True
                break
        if not match:
            raise SyntaxError(f"Unexpected character at position {pos}: {source[pos]}")
    return tokens

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()
