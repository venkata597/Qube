import sys
from lexer import read_file, tokenize
from parser import Parser

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.qube>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        source = read_file(filename)
        tokens = tokenize(source)
        parser = Parser(tokens)
        ir = parser.parse()
        print("\n--- Intermediate Representation (IR) ---")
        print(ir)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
