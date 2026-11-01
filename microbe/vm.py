from dataclasses import dataclass
from microbe.nodes import Function
import microbe.opcodes as opc

# microbe vm
# by las-r

# label resolver
def resolveLabels(stream):
    lbls = {}
    cleaned = []
    for item in stream:
        if item[0] == "LABEL":
            lbls[item[1]] = len(cleaned)
        else:
            cleaned.append(item)
    for inst in cleaned:
        opcode = inst[0]
        if opcode in (opc.jmp, opc.jmpifn) and isinstance(inst[1], str):
            inst[1] = lbls[inst[1]]
        elif opcode == opc.ld and isinstance(inst[1], Function):
            fnobj = inst[1]
            if isinstance(fnobj.entry, str):
                fnobj.entry = lbls[fnobj.entry]
    return cleaned

# block
@dataclass
class VMFrame:
    ret: int
    env: dict

# virtual machine
class MicrobeVM:
    def __init__(self, stream, natives):
        self.natives = natives
        self.globals = {}

        self.stream = resolveLabels(stream)
        self.ip = 0

        self.stack = []
        self.callstack = []

    def execute(self):
        # initial frame
        curf = VMFrame(None, self.globals)

        while self.ip < len(self.stream):
            # fetch
            inst = self.stream[self.ip]
            self.ip += 1

            # decode + execute
            match inst[0]:
                case opc.ld:
                    x = inst[1]
                    self.stack.append(x)

                case opc.pop:
                    self.stack.pop()

                case opc.varget:
                    var = inst[1]
                    if var in curf.env:
                        self.stack.append(curf.env[var])
                    elif var in self.globals:
                        self.stack.append(self.globals[var])
                    elif var in self.natives:
                        self.stack.append(var)

                case opc.varset:
                    var = inst[1]
                    curf.env[var] = self.stack.pop()

                case opc.unop:
                    op = inst[1]
                    x = self.stack.pop()
                    if op == "-": out = -x
                    elif op == "~": out = ~x
                    elif op == "!": out = int(not x)
                    self.stack.append(out)

                case opc.binop:
                    op = inst[1]
                    y = self.stack.pop()
                    x = self.stack.pop()
                    if op == "&&": out = int(x and y)
                    elif op == "||": out = int(x or y)
                    elif op == "+": out = x + y
                    elif op == "-": out = x - y
                    elif op == "*": out = x * y
                    elif op == "/": out = x / y
                    elif op == "%": out = x % y
                    elif op == "&": out = x & y
                    elif op == "|": out = x | y
                    elif op == "^": out = x ^ y
                    elif op == "==": out = int(x == y)
                    elif op == "<=": out = int(x <= y)
                    elif op == ">=": out = int(x >= y)
                    elif op == "<": out = int(x < y)
                    elif op == ">": out = int(x > y)
                    self.stack.append(out)

                case opc.arriget:
                    i = self.stack.pop()
                    arr = self.stack.pop()
                    self.stack.append(arr[i])

                case opc.arriset:
                    x = self.stack.pop()
                    i = self.stack.pop()
                    arr = self.stack.pop()
                    arr[i] = x

                case opc.jmp:
                    target = inst[1]
                    self.ip = target

                case opc.jmpifn:
                    target = inst[1]
                    cond = self.stack.pop()
                    if cond == 0:
                        self.ip = target

                case opc.call:
                    argc = inst[1]
                    fnobj = self.stack.pop()
                    if isinstance(fnobj, str) or fnobj in self.natives:
                        fnname = fnobj if isinstance(fnobj, str) else fnobj.__name__
                        args = [self.stack.pop() for _ in range(argc)][::-1]
                        self.stack.append(self.natives[fnname](*args))
                    elif isinstance(fnobj, Function):
                        args = [self.stack.pop() for _ in range(argc)][::-1]
                        lenv = {name: val for name, val in zip(fnobj.params, args)}
                        self.callstack.append(curf)
                        curf = VMFrame(self.ip, lenv)
                        self.ip = fnobj.entry

                case opc.ret:
                    self.ip = curf.ret
                    curf = self.callstack.pop()

                case opc.arr:
                    n = inst[1]
                    items = [self.stack.pop() for _ in range(n)][::-1]
                    self.stack.append(items)