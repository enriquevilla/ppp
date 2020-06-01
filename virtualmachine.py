from quadruples import Quadruples, Quadruple
from memory import Memory
from datastructures import variableTable
from error import *
import re
import numpy as np
cstMemMap = {}

globalMem = Memory()
localMem = Memory()
tempMem = Memory()

localMemStack = []
functionReturnStack = []
currentFunctionStack = []
pointerMemStack = []

def getValueFromAddress(address):
    add_type = address // 1000
    if add_type == 0:
        return globalMem.getInt(address)
    if add_type == 1:
        return globalMem.getFloat(address)
    if add_type == 2:
        return globalMem.getChar(address)
    if add_type == 3:
        return localMem.getInt(address)
    if add_type == 4:
        return localMem.getFloat(address)
    if add_type == 5:
        return localMem.getChar(address)
    if add_type == 6:
        return tempMem.getInt(address)
    if add_type == 7:
        return tempMem.getFloat(address)
    if add_type == 8:
        return tempMem.getChar(address)
    if add_type == 12:
        return pointerMemStack[address % 1000]
    else:
        return cstMemMap[address]

def runner_duckie():
    for cst in variableTable["constants"]:
        if "type" in variableTable["constants"][cst]:
            if variableTable["constants"][cst]["type"] == "int":
                cstMemMap[variableTable["constants"][cst]["address"]] = int(cst)
            elif variableTable["constants"][cst]["type"] == "float":
                cstMemMap[variableTable["constants"][cst]["address"]] = float(cst)
        else:
            cstMemMap[variableTable["constants"][cst]["address"]] = cst
    index = 0
    print(cstMemMap)
    # Quadruples.print_all()
    while len(Quadruples.quadruples) > index:    
        quad = Quadruples.quadruples[index]
        quad.print()
        newIndex = executeInstruction(quad)
        if newIndex:
            index = newIndex
        else:
            index += 1                    


def executeInstruction(quad):
    if quad.operator == "=":
        return assign(quad)
    elif quad.operator == "+":
        return add(quad)
    elif quad.operator == "-":
        return subtract(quad)
    elif quad.operator == "*":
        return multiply(quad)
    elif quad.operator == "/":
        return divide(quad)
    elif quad.operator == ">":
        return greaterThan(quad)
    elif quad.operator == "<":
        return lessThan(quad)
    elif quad.operator == "<>":
        return notEqual(quad)
    elif quad.operator == "==":
        return equals(quad)
    elif quad.operator == "|":
        return orOp(quad)
    elif quad.operator == "&":
        return andOp(quad)
    elif quad.operator == "read":
        return read(quad)
    elif quad.operator == "print":
        return printScreen(quad)
    elif quad.operator == "ENDFUNC":
        return endFunc(quad)
    elif quad.operator == "GOTOF":
        return gotof(quad)
    elif quad.operator == "GOTO":
        return goto(quad)
    elif quad.operator == "GOTO4":
        return goto4(quad)
    elif quad.operator == "GOSUB":
        return gosub(quad)
    elif quad.operator == "ERA":
        return era(quad)
    elif quad.operator == "PARAM":
        return param(quad)
    elif quad.operator == "RETURN":
        return rtn(quad)
    elif quad.operator == "VERIFY":
        return verify(quad)
    elif quad.operator == "ARR=":
        return arrAssign(quad)
    elif quad.operator == "ARR+":
        return arrAdd(quad)
    elif quad.operator == "ARR-":
        return arrSubtract(quad)
    elif quad.operator == "ARR*":
        return arrMultiply(quad)

def assign(quad):
    add_type = quad.result // 1000
    lOp = quad.left_operand // 1000
    if add_type == 0:
        if lOp == 12:
            globalMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 9:
            globalMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 6:
            globalMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        elif lOp == 3:
            globalMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        elif lOp == 0:
            globalMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)
    if add_type == 1:
        if lOp == 12:
            globalMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 10:
            globalMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 7:
            globalMem.insertFloat(tempMem.getFloat(quad.left_operand), quad.result)
        elif lOp == 4:
            globalMem.insertFloat(localMem.getFloat(quad.left_operand), quad.result)
        elif lOp == 1:
            globalMem.insertFloat(globalMem.getFloat(quad.left_operand), quad.result)
    if add_type == 2:
        if lOp == 12:
            globalMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 11:
            globalMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 8:
            globalMem.insertChar(tempMem.getChar(quad.left_operand), quad.result)
        elif lOp == 5:
            globalMem.insertChar(localMem.getChar(quad.left_operand), quad.result)
        elif lOp == 2:
            globalMem.insertChar(globalMem.getChar(quad.left_operand), quad.result)
    if add_type == 3:
        if lOp == 12:
            localMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 9:
            localMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 6:
            localMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        elif lOp == 3:
            localMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        elif lOp == 0:
            localMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)
    if add_type == 4:
        if lOp == 12:
            localMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 10:
            localMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 7:
            localMem.insertFloat(tempMem.getFloat(quad.left_operand), quad.result)
        elif lOp == 4:
            localMem.insertFloat(localMem.getFloat(quad.left_operand), quad.result)
        elif lOp == 1:
            localMem.insertFloat(globalMem.getFloat(quad.left_operand), quad.result)
    if add_type == 5:
        if lOp == 12:
            localMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 11:
            localMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 8:
            localMem.insertChar(tempMem.getChar(quad.left_operand), quad.result)
        elif lOp == 5:
            localMem.insertChar(localMem.getChar(quad.left_operand), quad.result)
        elif lOp == 2:
            localMem.insertChar(globalMem.getChar(quad.left_operand), quad.result)
    if add_type == 6:
        if lOp == 12:
            tempMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 9:
            tempMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 6:
            tempMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        elif lOp == 3:
            tempMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        elif lOp == 0:
            tempMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)
    if add_type == 7:
        if lOp == 12:
            tempMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 10:
            tempMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 7:
            tempMem.insertFloat(tempMem.getInt(quad.left_operand), quad.result)
        elif lOp == 4:
            tempMem.insertFloat(localMem.getInt(quad.left_operand), quad.result)
        elif lOp == 1:
            tempMem.insertFloat(globalMem.getInt(quad.left_operand), quad.result)
    if add_type == 8:
        if lOp == 12:
            tempMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        elif lOp == 11:
            tempMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        elif lOp == 8:
            tempMem.insertChar(tempMem.getInt(quad.left_operand), quad.result)
        elif lOp == 5:
            tempMem.insertChar(localMem.getInt(quad.left_operand), quad.result)
        elif lOp == 2:
            tempMem.insertChar(globalMem.getInt(quad.left_operand), quad.result)
    if add_type == 12:
        add_type = getValueFromAddress(quad.result)
        assign(Quadruple(quad.operator, quad.left_operand, "_", add_type))

def add(quad):
    res_address = quad.result // 1000
    # If operands are pointers to array spaces
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp + rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)
    # Address addition for array and matrix (base address + access index)
    elif res_address == 12:
        pointerMemStack.insert(quad.result % 1000, lOp + rOp)

def subtract(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp - rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

def multiply(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp * rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

def divide(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp / rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

def greaterThan(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp > rOp
    tempMem.insertInt(result, quad.result)

def lessThan(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp < rOp
    tempMem.insertInt(result, quad.result)

def notEqual(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp != rOp)
    tempMem.insertInt(result, quad.result)

def equals(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp == rOp)
    tempMem.insertInt(result, quad.result)

def orOp(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp or rOp)
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def andOp(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp and rOp)
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def read(quad):
    address = quad.result // 1000
    input_val = input()
    if re.match(r'[0-9]+\.[0-9]+', input_val):
        input_val = float(input_val)
        if address == 1:
            globalMem.insertFloat(input_val, quad.result)
        elif address == 4:
            localMem.insertFloat(input_val, quad.result)
    elif re.match(r'[0-9]+', input_val):
        input_val = int(input_val)
        if address == 0:
            globalMem.insertInt(input_val, quad.result)
        elif address == 3:
            localMem.insertInt(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')', input_val):
        input_val = input_val[1]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')', input_val):
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    else:
        input_val = input_val[0]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    
def printScreen(quad):
    if quad.result >= 12000:
        print(getValueFromAddress(getValueFromAddress(quad.result)))
    else:
        print(getValueFromAddress(quad.result))

def endFunc(quad):
    global localMem
    currentFunctionStack.pop()
    localMem = localMemStack.pop()
    return functionReturnStack.pop()

def gotof(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if lOp == 0:
        return quad.result

def goto(quad):
    return quad.result

def goto4(quad):
    conditionInt = Quadruples.quadruples[quad.result - 1].result
    localMem.insertInt(getValueFromAddress(conditionInt) + 1, conditionInt)
    return quad.result

def gosub(quad):
    global newMem
    global localMem
    localMem = newMem
    functionReturnStack.append(quad.id + 1)
    return quad.result

def era(quad):
    localMemStack.append(localMem)
    global newMem
    newMem = Memory()
    currentFunctionStack.append(quad.left_operand)

def param(quad):
    address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if address == 3:
        newMem.insertInt(lOp, quad.result)
    if address == 4:
        newMem.insertFloat(lOp, quad.result)
    if address == 5:
        newMem.insertChar(lOp, quad.result)    

def rtn(quad):
    address = quad.result // 1000
    rtn_address = Quadruples.quadruples[functionReturnStack[len(functionReturnStack) - 1]].result
    if quad.result >= 12000:
        rtnVal = getValueFromAddress(getValueFromAddress(quad.result))
    else:
        rtnVal = getValueFromAddress(quad.result)
    if address == 0 or address == 3 or address == 6 or address == 9:
        tempMem.insertInt(rtnVal, rtn_address)
        globalMem.insertInt(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    elif address == 1 or address == 4 or address == 7 or address == 10:
        tempMem.insertFloat(rtnVal, rtn_address)
        globalMem.insertFloat(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    else:
        tempMem.insertChar(rtnVal, rtn_address)
        globalMem.insertChar(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    newIndex = quad.id + 1
    if Quadruples.quadruples[newIndex].operator != "ENDFUNC":
        while Quadruples.quadruples[newIndex].operator != "ENDFUNC":
            newIndex += 1
        return newIndex

def verify(quad):
    arrType = quad.result // 1000
    if quad.left_operand >= 12000:
        check = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        check = getValueFromAddress(quad.left_operand)
    if check > quad.result - quad.right_operand:
        print("Error: index out of bounds.")
        exit(0)
        # Error.index_out_of_bounds()
    if arrType == 3:
        localMem.adjustIntArrSize(quad.result)
    elif arrType == 4:
        localMem.adjustFloatArrSize(quad.result)
    elif arrType == 5:
        localMem.adjustCharArrSize(quad.result)

def arrAssign(quad):
    arrType = quad.result["address"] // 1000
    spacesToAssign = quad.left_operand["rows"] * quad.left_operand["cols"]
    leftOpAddress = quad.left_operand["address"]
    for i in range(spacesToAssign):
        leftOp = getValueFromAddress(leftOpAddress)
        if arrType == 0:
            globalMem.insertInt(leftOp, quad.result["address"] + i)
        elif arrType == 1:
            globalMem.insertFloat(leftOp, quad.result["address"] + i)
        elif arrType == 2:
            globalMem.insertChar(leftOp, quad.result["address"] + i)
        elif arrType == 3:
            localMem.insertInt(leftOp, quad.result["address"] + i)
        elif arrType == 4:
            localMem.insertFloat(leftOp, quad.result["address"] + i)
        elif arrType == 5:
            localMem.insertChar(leftOp, quad.result["address"] + i)
        leftOpAddress += 1

def arrAdd(quad):
    arrType = quad.result // 1000
    spacesToAdd = quad.left_operand["rows"] * quad.left_operand["cols"]
    if quad.left_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToAdd)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToAdd)
    if quad.right_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToAdd)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToAdd)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    for i in range(spacesToAdd):
        leftOp = getValueFromAddress(leftOpAddress)
        rightOp = getValueFromAddress(rightOpAddress)
        if arrType == 6:
            tempMem.insertInt(leftOp + rightOp, quad.result + i)
        elif arrType == 7:
            tempMem.insertFloat(leftOp + rightOp, quad.result + i)
        leftOpAddress += 1
        rightOpAddress += 1

def arrSubtract(quad):
    arrType = quad.result // 1000
    spacesToSubtract = quad.left_operand["rows"] * quad.left_operand["cols"]
    if arrType == 6:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToSubtract)
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToSubtract)
    elif arrType == 7:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToSubtract)
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToSubtract)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    for i in range(spacesToSubtract):
        leftOp = getValueFromAddress(leftOpAddress)
        rightOp = getValueFromAddress(rightOpAddress)
        if arrType == 6:
            tempMem.insertInt(leftOp - rightOp, quad.result + i)
        elif arrType == 7:
            tempMem.insertFloat(leftOp - rightOp, quad.result + i)
        leftOpAddress += 1
        rightOpAddress += 1

def arrMultiply(quad):
    arrType = quad.result // 1000
    spacesToMultiply = quad.left_operand["rows"] * quad.left_operand["rows"]
    if quad.left_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToMultiply)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToMultiply)
    if quad.right_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToMultiply)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToMultiply)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    leftOpArray = np.zeros((quad.left_operand["rows"], quad.left_operand["cols"]))
    memoryIterator = 0
    for i in range(quad.left_operand["cols"]):
        for j in range(quad.left_operand["rows"]):
            leftOpArray[j][i] = getValueFromAddress(leftOpAddress + memoryIterator)
            memoryIterator += 1
    memoryIterator = 0
    rightOpArray = np.zeros((quad.right_operand["rows"], quad.right_operand["cols"]))
    for i in range(quad.right_operand["cols"]):
        for j in range(quad.right_operand["rows"]):
            rightOpArray[j][i] = getValueFromAddress(rightOpAddress + memoryIterator)
            memoryIterator += 1
    resultArray = np.dot(leftOpArray, rightOpArray)
    memoryIterator = 0
    arrayIterator = 0
    for i in range(len(resultArray[0])):
        for j in range(len(resultArray)):
            if arrType == 6:
                tempMem.insertInt(int(resultArray[j][arrayIterator]), quad.result + memoryIterator)
                memoryIterator += 1
            elif arrType == 7:
                tempMem.insertInt(resultArray[j][arrayIterator], quad.result + memoryIterator)
                memoryIterator += 1
        arrayIterator += 1
