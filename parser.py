import lexer as lexer
import ply.yacc as yacc
from datastructures import *
from quadruples import *
from error import Error
from virtualmachine import runner_duckie

tokens = lexer.tokens
arrMatId = Stack()
arrMatScope = Stack()

def p_program(t):
	'program : PROGRAM ID globalTable SEMICOLON declaration programFunc main'
	print("Code valid")
	# show variable table and function directory
	# print()
	# print(variableTable["constants"])
	# for i in functionDir:
	# 	print("\tfunction name: %s" % i)
	# 	print("\t\ttype: %s" % functionDir[i]["type"])
	# 	print("\t\tvars: %s" % functionDir[i]["vars"])
	# 	if "params" in functionDir[i]:
	# 		print("\t\tparams: %s" % functionDir[i]["params"].values())
	# 		print("\t\tparamsLength: %d" % functionDir[i]["paramsLength"])
	# 		print("\t\tstart: %d" % functionDir[i]["start"])
	# 		print("\t\tvarLength: %d" % functionDir[i]["varLength"])
	# 	print()
	
	# operands.print()
	# types.print()
	# operators.print()
	# Quadruples.print_all()
	# variableTable.clear()
	# arrMatOperands.print()

# global scope varTable
def p_globalTable(t):
	'globalTable : '
	variableTable["constants"] = {}
	# Initialize variableTable for global and set program name and type
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Initialize functionDir for global scope
	functionDir[currentScope] = {}
	# Set type and vars as reference to variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]
	tmp_quad = Quadruple("GOTO", "_", "_", "_")
	Quadruples.push_quad(tmp_quad)
	Quadruples.push_jump(-1)

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

def p_main(t):
	'main : mainTable MAIN LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'

# main scope varTable
def p_mainTable(t):
	'mainTable : '
	global currentScope
	# Add main to current scope varTable
	variableTable[currentScope]["main"] = {"type": "void"}
	currentScope = "main"
	# Initialize variableTable and functionDir for main scope
	variableTable[currentScope] = {}
	functionDir[currentScope] = {}
	# Set function type and vars as reference to variableTable["main"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]
	Quadruples.update_jump_quad(Quadruples.pop_jump(), Quadruples.next_id)

def p_assignment(t):
	'assignment : ID dimArray EQUAL hyperExpression SEMICOLON'
	# If id is in currentScope, generate quadruple and set its value in varTable
	if arrMatOperands.size() > 0:
		types.pop()
		assign = arrMatOperands.pop()
		address = arrMatOperands.pop()
		temp_quad = Quadruple("ARR=", assign, "_", address)
		Quadruples.push_quad(temp_quad)
	elif t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			if "rows" in variableTable[currentScope][t[1]]:
				types.pop()
				assign = operands.pop()
				address = operands.pop()
				temp_quad = Quadruple("=", assign, "_", address)
			else:
				address = variableTable[currentScope][t[1]]["address"]
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				operands.pop()
			Quadruples.push_quad(temp_quad)
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	# If id is in global scope, generate quadruple and set its value in varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			if "rows" in variableTable["global"][t[1]]:
				types.pop()
				assign = operands.pop()
				address = operands.pop()
				temp_quad = Quadruple("=", assign, "_", address)
			else:
				address = variableTable["global"][t[1]]["address"]
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				operands.pop()
			Quadruples.push_quad(temp_quad)
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	else:
		Error.undefined_variable(t[1], t.lexer.lineno - 1)

def p_declaration(t):
	'''declaration : VAR declarationPrim
				   | '''
	# Set start quadruple start for function
	functionDir[currentScope]["start"] = Quadruples.next_id

def p_declarationPrim(t):
	'''declarationPrim : primitive vars SEMICOLON declarationPrim
					   | '''

def p_primitive(t):
	'''primitive : INT
				 | FLOAT
				 | CHAR '''
	# When stating type, change currentType for declaration
	global currentType
	currentType = t[1]

def p_return(t):
	'return : RETURN LEFTPAR hyperExpression RIGHTPAR SEMICOLON'

def p_if(t):
	'if : IF LEFTPAR hyperExpression RIGHTPAR createJumpQuadIf THEN LEFTBRACE statement RIGHTBRACE ifElse updateJumpQuad'

def p_createJumpQuadIf(t):
	'createJumpQuadIf : '
	result_type = types.pop()
	# Check type and value for the evaluated expression and generate quadruple
	if result_type == "int":
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
	else: 
		Error.condition_type_mismatch(t.lexer.lineno)

def p_updateJumpQuad(t):
	'updateJumpQuad : '
	# Update gotof quadruples
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : ELSE createJumpQuadElse LEFTBRACE statement RIGHTBRACE
			  | '''

def p_createJumpQuadElse(t):
	'createJumpQuadElse : '
	# Create quadruple for else
	operator = "GOTO"
	tmp_quad = Quadruple(operator, '_', '_', '_')
	Quadruples.push_quad(tmp_quad)

	tmp_false = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_false, tmp_count)
	Quadruples.push_jump(-1)

def p_comment(t):
	'comment : COMMENT_TEXT'

def p_while(t):
	'while : WHILE pushLoopJump LEFTPAR hyperExpression RIGHTPAR beginLoopAction LEFTBRACE statement RIGHTBRACE endLoopAction'

def p_pushLoopJump(t):
	'pushLoopJump : '
	Quadruples.push_jump(1)

def p_beginLoopAction(t):
	'beginLoopAction : '
	result_type = types.pop()
	# Check expression type and value and add quadruple to stack
	if result_type == "int":
		res = operands.pop()
		operator = "GOTOF"
		# Generate Quadruple and push it to the list
		tmp_quad = Quadruple(operator, res, "_", "_")
		Quadruples.push_quad(tmp_quad)
		# Push into jump stack
		Quadruples.push_jump(-1)
	else:
		Error.condition_type_mismatch(t.lexer.lineno)

def p_endLoopAction(t):
	'endLoopAction : '
	# Generate quadruple when while finishes and update gotof
	false_jump = Quadruples.pop_jump()
	return_jump = Quadruples.pop_jump()
	tmp_quad = Quadruple("GOTO", "_", "_", return_jump-1)
	Quadruples.push_quad(tmp_quad)
	next_id = Quadruples.next_id
	Quadruples.update_jump_quad(false_jump, next_id)

def p_for(t):
	'for : FOR forAssignment TO insertJumpFor hyperExpression createQuadFor LEFTBRACE statement RIGHTBRACE updateQuadFor'

def p_insertJumpFor(t):
	'insertJumpFor : '
	Quadruples.push_jump(0)

def p_createQuadFor(t):
	'createQuadFor : '
	result_type = types.pop()
	# Check expression type and value and add quadruple to stack
	if result_type == "int":
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
	else: 
		Error.condition_type_mismatch(t.lexer.lineno)

def p_updateQuadFor(t):
	'updateQuadFor : '
	# Update gotof quadruple when for finishes
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTO4", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT addTypeInt'
	address_type = "cInt"
	cstAddress = 0
	if t[3] not in variableTable["constants"]:
		variableTable["constants"][t[3]] = {"address": addresses[address_type], "type": "int"}
		cstAddress = addresses[address_type]
		addresses[address_type] += 1
	else:
		cstAddress = variableTable["constants"][t[3]]["address"]
	if "rows" not in variableTable[currentScope][t[1]]:
		# Check if id exists in currentScope and set its value
		if t[1] in variableTable[currentScope]:
			address = variableTable[currentScope][t[1]]["address"]
			temp_quad = Quadruple("=", cstAddress, '_', address)
			Quadruples.push_quad(temp_quad)
		# Check if id exists in global scope and set its value
		elif t[1] in variableTable["global"]:
			address = variableTable["global"][t[1]]["address"]
			temp_quad = Quadruple("=", t[3], '_', address)
			Quadruples.push_quad(temp_quad)
		else:
			Error.undefined_variable(t[1], t.lexer.lineno)
	else:
		print("Error: invalid assignment to non-atomic variable in line %d." % (t.lexer.lineno))
		exit(0)
		# Error class call

def p_vars(t):
	'vars : ID addVarsToTable varsArray varsComa'
	global arrMatId
	while arrMatId.size() > 0:
		arrMatId.pop()

def p_addVarsToTable(t):
	'addVarsToTable : '
	# If current ID (t[-1]) exists in scope or global, throw error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Add current ID (t[-1]) to variableTable[scope]
		variableTable[currentScope][t[-1]] = {"type": currentType}
		address_type = "g"
		if currentScope != "global":
			address_type = "l"
		if currentType == "int":
			address_type += "Int"
		elif currentType == "float":
			address_type += "Float"
		else:
			address_type += "Char"
		variableTable[currentScope][t[-1]]["address"] = addresses[address_type]
		addresses[address_type] += 1
		global arrMatId
		arrMatId = Stack()
		arrMatId.push(t[-1])

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''
	global arrMatId

def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setRows varsMatrix 
				 | '''
	address_type = "g"
	const_address = "c"
	if currentScope != "global":
		address_type = "l"
	if currentType == "int":
		address_type += "Int"
		const_address += "Int"
	if currentType == "float":
		address_type += "Float"
		const_address += "Float"
	if currentType == "char":
		address_type += "Char"
		const_address += "Char"
	global arrMatId
	arrMatAddress = variableTable[currentScope][arrMatId.peek()]["address"]
	if "rows" in variableTable[currentScope][arrMatId.peek()] and "cols" not in variableTable[currentScope][arrMatId.peek()]:
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		addresses[address_type] += rows - 1
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		addresses[const_address] += 1
	if "cols" in variableTable[currentScope][arrMatId.peek()]:
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		cols = variableTable[currentScope][arrMatId.peek()]["cols"]
		addresses[address_type] += rows * cols - 1
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		addresses[const_address] += 1

def p_setRows(t):
	'setRows : '
	global arrMatId
	if int(t[-3]) > 0:
		variableTable[currentScope][arrMatId.peek()]["rows"] = int(t[-3])
		operands.pop()
		types.pop()
	else:
		print("Error: array '%s' size in line %d must be positive." % (arrMatId.peek(), t.lexer.lineno))
		exit(0)
		# Error.non_positive_sized_array(arrMatId.peek(), t.lexer.lineno)

def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setCols
				  | '''

def p_setCols(t):
	'setCols : '
	global arrMatId
	if int(t[-3]) > 0:
		variableTable[currentScope][arrMatId.peek()]["cols"] = int(t[-3])
		operands.pop()
		types.pop()
	else:
		print("Error: array '%s' size in line %d must be positive." % (arrMatId.peek(), t.lexer.lineno))
		exit(0)
		# Error.non_positive_sized_array(arrMatId.peek(), t.lexer.lineno)

def p_function(t):
	'function : functionType ID addFuncToDir LEFTPAR param RIGHTPAR setParamLength LEFTBRACE declaration statement RIGHTBRACE'
	# When exiting function scope, reset scope to global and delete variableTable and reference to it in functionDir
	global currentScope
	# del variableTable[currentScope]
	# del functionDir[currentScope]["vars"]
	# Create endfunc quadruple for function end
	temp_quad = Quadruple("ENDFUNC", "_", "_", "_")
	Quadruples.push_quad(temp_quad)
	# Temporary variables = function quad length as maximum and reset func_quads
	functionDir[currentScope]["varLength"] = len(functionDir[currentScope]["vars"])
	Quadruples.func_quads = 0
	currentScope = "global"
	# Reset local addresses
	addresses["lInt"] -= addresses["lInt"] % 1000
	addresses["lFloat"] -= addresses["lFloat"] % 1000
	addresses["lChar"] -= addresses["lChar"] % 1000
	types.pop()

def p_addFuncToDir(t):
	'addFuncToDir : '
	# If function exists in global scope, throw an error
	if t[-1] in variableTable["global"]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		global currentScope
		global currentType
		# Add function to variableTable of currentScope
		variableTable["global"][t[-1]] = {"type": currentType}
		if currentType == "int":
			address = addresses["gInt"]
			addresses["gInt"] += 1
		elif currentType == "float":
			address = addresses["gFloat"]
			addresses["gFloat"] += 1
		elif currentType == "char":
			address = addresses["gChar"]
			addresses["gChar"] += 1
		variableTable["global"][t[-1]]["address"] = address
		# Change scope to new function id
		currentScope = t[-1]
		# Initialize variableTable and functionDir for new function id
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Set new function type and vars as reference to variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]
		functionDir[currentScope]["params"] = Queue()

def p_functionType(t):
	'''functionType : FUNCTION primitive
					| FUNCTION VOID setVoidType '''

def p_setVoidType(t):
	'setVoidType : '
	# Set void as currentType
	global currentType
	currentType = t[-1]

def p_param(t):
	'''param : primitive ID addFuncParams functionParam
			 | '''

def p_addFuncParams(t):
	'addFuncParams : '
	# If function param exists in scope, throw error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Add function param to variableTable of currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
		if currentType == "int":
			variableTable[currentScope][t[-1]]["address"] = addresses["lInt"]
			addresses["lInt"] += 1
		elif currentType == "float":
			variableTable[currentScope][t[-1]]["address"] = addresses["lFloat"]
			addresses["lFloat"] += 1
		else:
			variableTable[currentScope][t[-1]]["address"] = addresses["lChar"]
			addresses["lChar"] += 1
		if "params" not in functionDir[currentScope]:
			functionDir[currentScope]["params"] = Queue()
		# Insert currentTypes into params Queue
		functionDir[currentScope]["params"].enqueue(currentType)

def p_setParamLength(t):
	'setParamLength : '
	# Set the function param number to the size of params Queue
	functionDir[currentScope]["paramsLength"] = functionDir[currentScope]["params"].size()

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

def p_cst_prim(t):
	'''cst_prim : CST_INT addTypeInt
				| CST_FLOAT addTypeFloat
				| CST_CHAR addTypeChar'''
	t[0] = t[1]

def p_addTypeInt(t):
	'addTypeInt : '
	types.push("int")
	address_type = "cInt"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "int"}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

def p_addTypeFloat(t):
	'addTypeFloat : '
	types.push("float")
	address_type = "cFloat"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "float"}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

def p_addTypeChar(t):
	'addTypeChar : '
	types.push("char")
	address_type = "cChar"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type]}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

def p_hyperExpression(t):
	'''hyperExpression : superExpression evaluateHE opHyperExpression hyperExpressionNested
					   | superExpression opMatrix
					   | superExpression evaluateHE'''

def p_hyperExpressionNested(t):
	'''hyperExpressionNested : superExpression evaluateHE opHyperExpression hyperExpressionNested
							 | superExpression evaluateHE'''

def p_evaluateHE(t):
	'evaluateHE : '
	if operators.size() != 0:
		# Generate quadruple for or/and expressions
		if operators.peek() == "|" or operators.peek() == "&":
			# Pop operands
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop operators
			oper = operators.pop()
			# Pop types
			rType = types.pop()
			lType = types.pop()
			# Check semanticCube with types and operator
			resType = semanticCube[(lType, rType, oper)]
			# Check type and value
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)

def p_opMatrix(t):
	'''opMatrix : EXCLAMATION addOperator
				| QUESTION addOperator
				| DOLLARSIGN addOperator '''

def p_opHyperExpression(t):
	'''opHyperExpression : AND addOperator
						 | OR addOperator '''

def p_superExpression(t):
	'''superExpression : exp evaluateSE opSuperExpression exp evaluateSE
					   | exp evaluateSE '''

def p_evaluateSE(t):
	'evaluateSE : '
	if operators.size() != 0:
		# Generate quadruple for comparison operators
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==":
			# Pop operands
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop operator
			oper = operators.pop()
			# Pop types
			rType = types.pop()
			lType = types.pop()
			# Check semanticCube for types and operator
			resType = semanticCube[(lType, rType, oper)]
			# Check result type and evaluate expression
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)

def p_opSuperExpression(t):
	'''opSuperExpression : GT addOperator
						 | LT addOperator
						 | NOTEQUAL addOperator 
						 | ISEQUAL addOperator'''

def p_exp(t):
	'''exp : term evaluateTerm expFunction
		   | term evaluateTerm '''

def p_evaluateTerm(t):
	'evaluateTerm : '
	if operators.size() != 0:
		# Generate quadruple for add/subtract operators
		if operators.peek() == "+" or operators.peek() == "-":
			# Pop operands
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop operator
			oper = operators.pop()
			# Pop types
			rType = types.pop()
			lType = types.pop()
			# Check semanticCube with types and operator
			resType = semanticCube[(lType, rType, oper)]
			# Check and validate for array or matrix operands and sizes
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validate equal dimensions
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				if lId["rows"] == rId["rows"] and lId["cols"] == rId["cols"]:
					if oper == "+":
						oper = "ARR+"
					else:
						oper = "ARR-"
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				else:
					print("Error: operation between variables with dimensions that don't match in line %d." % (t.lexer.lineno))
					exit(0)
					# Error class call
			elif arrMatOperands.size() == 1:
				print("Error: invalid operation in line %d." % (t.lexer.lineno))
				exit(0)
				# Error class call
			# Check result type and evaluate expression
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				if oper == "ARR+" or oper == "ARR-":
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": lOp["cols"]
					})
					addresses[address_type] += lOp["rows"] * lOp["cols"]
				else:
					addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)

def p_expFunction(t):
	'''expFunction : PLUS addOperator exp
				   | MINUS addOperator exp '''

def p_term(t):
	'''term : factor evaluateFactor termFunction
			| factor evaluateFactor '''

def p_evaluateFactor(t):
	'evaluateFactor : '
	if operators.size() != 0:
		# Generate quadruple for multiplication/division operators
		if operators.peek() == "*" or operators.peek() == "/":
			# Pop operands
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop operator
			oper = operators.pop()
			# Pop types
			rType = types.pop()
			lType = types.pop()
			# Check semanticCube with types and operator
			resType = semanticCube[(lType, rType, oper)]
			# Check and validate for array or matrix operands and sizes
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validate equal dimensions
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				if lId["rows"] == rId["rows"] and lId["cols"] == rId["cols"]:
					if oper == "*":
						oper = "ARR*"
					else:
						print("Error: invalid operator on arrays in line %d." % (t.lexer.lineno))
						exit(0)
						# Error class call
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				else:
					print("Error: operation between variables with dimensions that don't match in line %d." % (t.lexer.lineno))
					exit(0)
					# Error class call
			elif arrMatOperands.size() == 1:
				print("Error: invalid operation in line %d." % (t.lexer.lineno))
				exit(0)
				# Error class call
			# Check result type and evaluate expression
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				if oper == "ARR*":
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": lOp["cols"]
					})
					addresses[address_type] += lOp["rows"] * lOp["cols"]
				else:
					addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)

def p_termFunction(t):
	'''termFunction : MULTIPLY addOperator term
					| DIVIDE addOperator term '''

def p_addOperator(t):
	'addOperator : '
	# Add any received operator to stack
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR addFF hyperExpression RIGHTPAR removeFF
			  | cst_prim 
			  | module
			  | ID dimArray'''

def p_addFF(t):
	'addFF : '
	# Add "fondo falso" for priority
	operators.push("(")

def p_removeFF(t):
	'removeFF : '
	# Remove "fondo falso"
	operators.pop()

def p_read(t):
	'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
	'id_list : ID dimArray addRead id_listFunction'

def p_addRead(t):
	'addRead : '
	# Generate read quadruple
	if t[-2] in variableTable[currentScope]:
		address = variableTable[currentScope][t[-1]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	elif t[-2] in variableTable["global"]:
		address = variableTable["global"][t[-1]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	else:
		Error.undefined_variable(t[-2], t.lexer.lineno)

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

def p_print(t):
	'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'printFunction2 : printFunction'

def p_print_param(t):
	'''print_param : hyperExpression addPrint
				   | CST_STRING addPrintString '''

def p_addPrint(t):
	'addPrint : '
	# Generate print quadruple
	if arrMatOperands.size() > 0:
		print("Error: invalid print on array variable in line %d." % (t.lexer.lineno))
		exit(0)
	temp_quad = Quadruple("print", '_', '_', operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()

def p_addPrintString(t):
	'addPrintString : '
	# Add string to print quadruple
	address = 0
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses["cChar"]}
		address = variableTable["constants"][t[-1]]["address"]
		addresses["cChar"] += 1
	else:
		address = variableTable["constants"][t[-1]]["address"]
	temp_quad = Quadruple("print", '_', '_', address)
	Quadruples.push_quad(temp_quad)

def p_statement(t):
	'''statement : return checkVoidType
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module SEMICOLON statement
				 | for statement
				 | while statement
				 | checkNonVoidType'''

def p_checkVoidType(t):
	'checkVoidType : '
	global currentScope
	if functionDir[currentScope]["type"] == "void":
		Error.return_on_void_function(0, t.lexer.lineno)
	else:
		tmp_quad = Quadruple("RETURN", "_", "_", operands.pop())
		Quadruples.push_quad(tmp_quad)

def p_checkNonVoidType(t):
	'checkNonVoidType : '
	if functionDir[currentScope]["type"] != "void":
		Error.no_return_on_function(0, t.lexer.lineno)

def p_module(t):
	'module : ID checkFuncExists genERASize LEFTPAR moduleFunction nullParam RIGHTPAR genGosub'

def p_checkFuncExists(t):
	'checkFuncExists : '
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	global funcName
	funcName = t[-1]
	operators.push("module")
	types.push(functionDir[funcName]["type"])

def p_genERASize(t):
	'genERASize : '
	global funcName
	tmp_quad = Quadruple("ERA", variableTable["global"][funcName]["address"], "_", "_")
	Quadruples.push_quad(tmp_quad)
	global paramNum
	paramNum = 1

def p_nullParam(t):
	'nullParam : '
	global paramNum
	global funcName
	if paramNum < len(functionDir[funcName]["params"].values()):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)

def p_genGosub(t):
	'genGosub : '
	global funcName
	tmp_quad = Quadruple("GOSUB", variableTable["global"][funcName]["address"], "_", functionDir[funcName]["start"])
	Quadruples.push_quad(tmp_quad)
	if functionDir[funcName]["type"] != "void":
		if functionDir[funcName]["type"] == "int":
			tmpAddress = addresses["tInt"]
			addresses["tInt"] += 1
		if functionDir[funcName]["type"] == "float":
			tmpAddress = addresses["tFloat"]
			addresses["tFloat"] += 1
		if functionDir[funcName]["type"] == "char":
			tmpAddress = addresses["tChar"]
			addresses["tChar"] += 1
		tmp_quad = Quadruple("=", variableTable["global"][funcName]["address"], "_", tmpAddress)
		Quadruples.push_quad(tmp_quad)
		operands.push(tmpAddress)
		types.push(variableTable["global"][funcName]["type"])
	operators.pop()
	types.pop()

def p_moduleFunction(t):
	'''moduleFunction : hyperExpression genParam nextParam COMA moduleFunction
					  | hyperExpression genParam 
					  | '''

def p_genParam(t):
	'genParam : '
	global funcName
	global paramNum
	if arrMatOperands.size() > 0:
		print("Error: array parameter in module call in in line %d." % (t.lexer.lineno))
		exit(0)
	arg = operands.pop()
	argType = types.pop()
	paramList = functionDir[funcName]["params"].values()
	counter = paramNum
	if paramNum > len(paramList):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)
	if argType == paramList[-paramNum]:
		for var in functionDir[funcName]["vars"]:
			if counter == 1:
				address = functionDir[funcName]["vars"][var]["address"]
			counter -= 1
		tmp_quad = Quadruple("PARAM", arg, '_', address)
		Quadruples.push_quad(tmp_quad)
	else:
		Error.type_mismatch_module(funcName, t.lexer.lineno)

def p_nextParam(t):
	'nextParam : '
	global paramNum
	paramNum += 1

def p_dimArray(t):
	'''dimArray : addOperandId addTypeId LEFTBRACK readIDType hyperExpression verifyRows RIGHTBRACK dimMatrix
				| addOperandId addTypeId '''
	global arrMatId
	arrMatId.pop()
	arrMatScope.pop()

def p_addOperandId(t):
	'addOperandId : '
	# Add dimensioned variable ID to a stack
	arrMatId.push(t[-1])
	# Add currentScope operand value to operand stack
	if arrMatId.peek() in variableTable[currentScope]:
		operands.push(variableTable[currentScope][arrMatId.peek()]["address"])
		arrMatScope.push(currentScope)
	# Add global scope operand value to operand stack
	elif arrMatId.peek() in variableTable["global"]:
		operands.push(variableTable["global"][arrMatId.peek()]["address"])
		arrMatScope.push("global")
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)
	if "rows" in variableTable[arrMatScope.peek()][t[-1]]:
		arrMatOperands.push(variableTable[arrMatScope.peek()][t[-1]])

def p_addTypeId(t):
	'addTypeId : '
	# Push types to types stack
	if arrMatId.peek() in variableTable[currentScope]:
		types.push(variableTable[currentScope][arrMatId.peek()]["type"])
	elif arrMatId.peek() in variableTable["global"]:
		types.push(variableTable["global"][arrMatId.peek()]["type"])
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)

def p_readIDType(t):
	'readIDType : '
	operands.pop()
	operators.push("Mat")
	arrMatOperands.pop()
	if types.pop() != variableTable[currentScope][arrMatId.peek()]["type"]:
		Error.type_mismatch(arrMatId.peek(), t.lexer.lineno)
	if "rows" not in variableTable[currentScope][arrMatId.peek()]:
		if "rows" not in variableTable["global"][arrMatId.peek()]:
			print("Error: variable '%s' in line %d is not subscriptable as an array." % (arrMatId.peek(), t.lexer.lineno))
			exit(0)
			# Error.not_subscriptable_array(arrMatId.peek(), t.lexer.lineno)

def p_verifyRows(t):
	'verifyRows : '
	if types.pop() != "int":
		print("Error: type mismatch in variable '%s' indexation in line %d." % (arrMatId.peek(), t.lexer.lineno))
		exit(0)
		# Error.type_mismatch_indexation(arrMatId.peek(), t.lexer.lineno)
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	upperLim = baseAdd + variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"] - 1
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	Quadruples.push_quad(tmp_quad)

def p_dimMatrix(t):
	'''dimMatrix : LEFTBRACK hyperExpression verifyCols RIGHTBRACK
				 | checkMatAsArray '''
	operators.pop()
	address_type = "t"
	if variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "int":
		address_type += "Int"
	elif variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "float":
		address_type += "Float"
	else:
		address_type += "Char"
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	addressCst = variableTable["constants"][baseAdd]["address"]
	tmp_quad = Quadruple("+", addressCst, operands.pop(), addresses["tPoint"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tPoint"])
	types.push(variableTable[arrMatScope.peek()][arrMatId.peek()]["type"])
	addresses["tPoint"] += 1

def p_verifyCols(t):
	'verifyCols : '
	if "cols" not in variableTable[arrMatScope.peek()][arrMatId.peek()]:
		print("Error: variable '%s' in line %d is not subscriptable as a matrix." % (arrMatId, t.lexer.lineno))
		exit(0)
		# Error.not_subscriptable_matrix(arrMatId.peek(), t.lexer.lineno)
	#TODO TEST MIXING GLOBAL/LOCAL ARRAYS
	if types.pop() != "int":
		print("Error: type mismatch in variable '%s' indexation in line %d." % (arrMatId.peek(), t.lexer.lineno))
		exit(0)
		# Error.type_mismatch_indexation(arrMatId.peek(), t.lexer.lineno)
	# Address calculation formula for C-style array and matrix 
	constant_value = str(variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"])
	cstIntAddr = variableTable["constants"][constant_value]["address"]
	tmp_quad = Quadruple("*", operands.pop(), cstIntAddr, addresses["tInt"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tInt"])
	addresses["tInt"] += 1
	tmp_quad = Quadruple("+", operands.pop(), operands.pop(), addresses["tInt"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tInt"])
	addresses["tInt"] += 1
	#[1, [4  [7, [10,
	# 2,  5,  8,  11,
	# 3], 6], 9], 12]
	# Addre = [0,1,2,3,4,5,6,7,8,9,10,11]
	# Datos = [1,2,3,4,5,6,7,8,9,10,11,12]
	#[2][2] => 9 => address = 8 
	#[1][0] => 8 => address = 7
	# 1st + 2nd * rows
	baseAdd = variableTable[currentScope][arrMatId.peek()]["address"]
	upperLim = baseAdd + variableTable[currentScope][arrMatId.peek()]["rows"] * variableTable[currentScope][arrMatId.peek()]["cols"] - 1
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	Quadruples.push_quad(tmp_quad)

def p_checkMatAsArray(t):
	'checkMatAsArray : '
	global arrMatId
	if "cols" in variableTable[currentScope][arrMatId.peek()]:
		print("Error: matrix '%s' accessed as an array in line %d." % (arrMatId.peek(), t.lexer.lineno))
		exit(0)
		# Error.matrix_as_array(arrMatId.peek(), t.lexer.lineno)

def p_error(t):
	Error.syntax(t.value, t.lexer.lineno)

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)

runner_duckie()