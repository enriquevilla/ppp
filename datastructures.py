currentScope = "global"
currentType = "program"

functionDir = {}
variableTable = {}
semanticCube = {}
quadruples = []
operators = []
operands = []
types = []
temp = 1
ty = {
    0: "int",
    1: "float",
    2: "char"
}
ops = ["+", "-", "*", "/"]

# print("Semantic Cube: ")
for i in ty:
    for j in ty:
        for k in ops:
            if i > j:
                semanticCube[(ty[i], ty[j], k)] = ty[i]
            else:
                semanticCube[(ty[i], ty[j], k)] = ty[j]
            if k != "+" and (ty[i] == "char" or ty[j] == "char"):
                semanticCube[(ty[i], ty[j], k)] = "error"
            # print("%s %s %s = %s" % (types[i], k, types[j], semanticCube[(types[i], types[j], k)]))

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