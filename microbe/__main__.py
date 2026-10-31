import sys
from microbe import lexer
from microbe import parser
from microbe import nodes
from microbe import vm

# microbe
# forked from micro
# by las-r

# native functions
def ibtype(x):
    if isinstance(x, list): return "arr"
    if isinstance(x, float): return "float"
    if isinstance(x, nodes.Function) or callable(x): return "func"
    if isinstance(x, int): return "int"
    if isinstance(x, str): return "str"
    
def ibconv(x, t):
    if t == "arr": return list(x)
    if t == "float": return float(x)
    if t == "int": return int(x)
    if t == "str": return str(x)
    raise Exception(f"Unknown convertible type: {t}")

def ibadd(a, i, x):
    ac = a.copy()
    ac.insert(i, x)
    return ac

def ibdel(a, i):
    ac = a.copy()
    ac.pop(i)
    return ac

def main():
    # open code
    if len(sys.argv) < 2:
        print("usage: python -m microbe <file.mic>")
        return
    file = sys.argv[1]
    with open(file) as f:
        code = f.read()

    # compile
    tokens = lexer.tokenize(code)
    nodes = parser.parse(tokens)
    stream = []
    for n in nodes:
        n.compile(stream)

    # native functions
    natives = {
        "print": print,
        "input": input,
        "type": ibtype,
        "conv": ibconv,
        "len": len,
        "add": ibadd,
        "del": ibdel
    }

    # vm
    mvm = vm.MicrobeVM(stream, natives)
    vm.execute()
        
if __name__ == "__main__":
    main()