
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def print(self):
        print(self.items)

currentScope = "global"
currentType = "program"

functionDir = {}
variableTable = {}
semanticCube = {}
quadruples_original = Stack()
operators = Stack()
operands = Stack()
types = Stack()
temp = 1
ty = {
    0: "int",
    1: "float",
    2: "char"
}
ops = ["+", "-", "*", "/", ">", "<", "<>", "==", "&", "|"]

# print("Semantic Cube: ")
for i in ty:
    for j in ty:
        for k in ops:
            if i > j:
                semanticCube[(ty[i], ty[j], k)] = ty[i]
            else:
                semanticCube[(ty[i], ty[j], k)] = ty[j]
            if k != "+" and (i == 2 or j == 2):
                semanticCube[(ty[i], ty[j], k)] = "error"
            if k == ">" or k == "<" or k == "<>" or k == "==" or k == "|" or k == "&":
                if (i == 0 or i == 1) and (j == 0 or j == 1):
                    semanticCube[(ty[i], ty[j], k)] = "int"
                else:
                    semanticCube[(ty[i], ty[j], k)] = "error"
            if k == "<>" or k == "==":
                if i == 2 and j == 2:
                    semanticCube[(ty[i], ty[j], k)] = "int"
            # print("%s %s %s = %s" % (ty[i], k, ty[j], semanticCube[(ty[i], ty[j], k)]))

# functionDir visual example
'''
    "global": {
        "type": "void",
        "vars": variableTable["global"] -> "i": {
                                                "type": "int"
                                                "value": 1
                                            }
                                            ...
    }
    "main": {
        "type": "void",
        "vars": variableTable["main"] -> "c": {
                                              "type": "char"
                                              "value": "h"
                                         }
                                         ...
    }
'''

# semanticCube explanation
'''
    keys are tuples => (operand1, operand2, operator)

    semanticCube[(op1, op2, op)] => int/float/char/error

    semanticCube[("int", "int", "+")] => "int"
    semanticCube[("char", "float", "*")] => "error"
'''
