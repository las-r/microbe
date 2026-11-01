import microbe.opcodes as opc

# microbe nodes
# forked from micro
# by las-r

# loop counter
loopc = 0
def get_unique_loop_id():
    global loopc
    loopc += 1
    return loopc

# function object
class Function:
    def __init__(self, params, entry):
        self.params = params
        self.entry = entry

# literal node
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def compile(self, stream):
        stream.append([opc.ld, self.value])

# variable nodes
class VariableNode:
    def __init__(self, name):
        self.name = name

    def compile(self, stream):
        stream.append([opc.varget, self.name])

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def compile(self, stream):
        self.expr.compile(stream)
        stream.append([opc.varset, self.name])

# operation nodes
class UnaryOpNode:
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def compile(self, stream):
        self.a.compile(stream)
        stream.append([opc.unop, self.op])

class BinaryOpNode:
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    def compile(self, stream):
        self.a.compile(stream)
        self.b.compile(stream)
        stream.append([opc.binop, self.op])

# array nodes
class ArrayNode:
    def __init__(self, items):
        self.items = items

    def compile(self, stream):
        for i in self.items:
            i.compile(stream)
        stream.append([opc.arr, len(self.items)])

class IndexNode:
    def __init__(self, arr, idx):
        self.arr = arr
        self.idx = idx

    def compile(self, stream):
        self.arr.compile(stream)
        self.idx.compile(stream)
        stream.append([opc.arriget])

class IndexAssignNode:
    def __init__(self, arr, idx, val):
        self.arr = arr
        self.idx = idx
        self.val = val

    def compile(self, stream):
        self.arr.compile(stream)
        self.idx.compile(stream)
        self.val.compile(stream)
        stream.append([opc.arriset])

# control flow nodes
class IfNode:
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody

    def compile(self, stream):
        ifid = get_unique_loop_id()
        elselbl = f"ELSE_START_{ifid}"
        endlbl = f"IF_END_{ifid}"
        self.cond.compile(stream)
        stream.append([opc.jmpifn, elselbl])
        for stmt in self.body:
            stmt.compile(stream)
        stream.append([opc.jmp, endlbl])
        stream.append(["LABEL", elselbl])
        if self.ebody:
            for stmt in self.ebody:
                stmt.compile(stream)
        stream.append(["LABEL", endlbl])

class WhileNode:
    def __init__(self, cond, body):
            self.cond = cond
            self.body = body

    def compile(self, stream):
        loopid = get_unique_loop_id()
        startlbl = f"WHILE_START_{loopid}"
        endlbl = f"WHILE_END_{loopid}"
        stream.append(["LABEL", startlbl])
        self.cond.compile(stream)
        stream.append([opc.jmpifn, endlbl])
        for stmt in self.body:
            stmt.compile(stream)
        stream.append([opc.jmp, startlbl])
        stream.append(["LABEL", endlbl])

class BreakNode:
    def __init__(self):
        pass

    def compile(self, stream):
        lbl = f"WHILE_END_{loopc}"
        stream.append([opc.jmp, lbl])

# function nodes
class FunctionNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def compile(self, stream):
        fnid = get_unique_loop_id()
        skiplbl = f"FUNC_SKIP_{fnid}"
        entrylbl = f"FUNC_ENTRY_{fnid}"
        stream.append([opc.jmp, skiplbl])
        stream.append(["LABEL", entrylbl])
        for stmt in self.body:
            stmt.compile(stream)
        stream.append([opc.ld, None])
        stream.append([opc.ret])
        stream.append(["LABEL", skiplbl])
        fnobj = Function(self.params, entrylbl)
        stream.append([opc.ld, fnobj])
        stream.append([opc.varset, self.name])

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def compile(self, stream):
        for arg in self.args:
            arg.compile(stream)
        stream.append([opc.varget, self.name])
        stream.append([opc.call, len(self.args)])

class ReturnNode:
    def __init__(self, expr):
        self.expr = expr

    def compile(self, stream):
        if self.expr:
            self.expr.compile(stream)
        else:
            stream.append([opc.ld, None])
        stream.append([opc.ret])