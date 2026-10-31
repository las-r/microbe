import opcodes as opc
from nodes import Function

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

# virtual machine
class MicrobeVM:
    def __init__(self, stream, natives):
        self.natives = natives
        self.stream = resolveLabels(stream)
        self.ip = 0