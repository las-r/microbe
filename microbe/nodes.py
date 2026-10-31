import opcodes as opc

# microbe nodes
# forked from micro
# by las-r

# exceptions
class Break(Exception):
    pass

class Return(Exception):
    def __init__(self, value):
        self.value = value

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
        pass

# variable nodes
class VariableNode:
    def __init__(self, name):
        self.name = name

    def compile(self, stream):
        pass

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def compile(self, stream):
        pass

# operation nodes
class UnaryOpNode:
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def compile(self, stream):
        pass

class BinaryOpNode:
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    def compile(self, stream):
        pass

# array nodes
class ArrayNode:
    def __init__(self, items):
        self.items = items

    def compile(self, stream):
        pass

class IndexNode:
    def __init__(self, arr, idx):
        self.arr = arr
        self.idx = idx

    def compile(self, stream):
        pass

class IndexAssignNode:
    def __init__(self, arr, idx, val):
        self.arr = arr
        self.idx = idx
        self.val = val

    def compile(self, stream):
        pass

# control flow nodes
class IfNode:
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody

    def compile(self, stream):
        pass

class WhileNode:
    def __init__(self, cond, body):
            self.cond = cond
            self.body = body

    def compile(self, stream):
        pass

class BreakNode:
    def __init__(self):
        pass

    def compile(self, stream):
        pass

# function nodes
class FunctionNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def compile(self, stream):
        pass

class CallNode:
    def __init__(self, name, args):
        self.name, self.args = name, args

    def compile(self, stream):
        pass

class ReturnNode:
    def __init__(self, expr):
        self.expr = expr

    def compile(self, stream):
        pass