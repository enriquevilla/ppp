import lexer as lexer
import ply.yacc as yacc
from datastructures import types, operands, operators, variableTable, Queue
from datastructures import functionDir, temp, currentScope, currentType, semanticCube
from quadruples import *

tokens = lexer.tokens

def p_program(t):
	'program : PROGRAM ID globalTable SEMICOLON programVars programFunc main'
	print("Code valid")
	# show variable table and function directory
	# print()
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
	
	operands.print()
	types.print()
	operators.print()
	Quadruples.print_all()
	variableTable.clear()

# global scope varTable
def p_globalTable(t):
	'globalTable : '
	# Initialize variableTable for global and set program name and type
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Initialize functionDir for global scope
	functionDir[currentScope] = {}
	# Set type and vars as reference to variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_programVars(t):
	'''programVars : globalDeclaration
				   | '''
	
def p_globalDeclaration(t):
	'globalDeclaration : VAR declarationPrim'

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

def p_assignment(t):
	'assignment : ID EQUAL hyperExpression SEMICOLON'
	# If id is in currentScope, generate quadruple and set its value in varTable
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.peek(), '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = operands.pop()
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	# If id is in global scope, generate quadruple and set its value in varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.peek(), '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable["global"][t[1]]["value"] = operands.pop()
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_declaration(t):
	'declaration : VAR declarationPrim'
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
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			temp_quad = Quadruple(operator, res, '_', '_')
			Quadruples.push_quad(temp_quad)
			Quadruples.push_jump(-1)
		else: 
			print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else: 
		print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

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
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			# Generate Quadruple and push it to the list
			tmp_quad = Quadruple(operator, res, "_", "_")
			Quadruples.push_quad(tmp_quad)
			# Push into jump stack
			Quadruples.push_jump(-1)
		else:
			print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)	
	else :
		print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)	

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
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			temp_quad = Quadruple(operator, res, '_', '_')
			Quadruples.push_quad(temp_quad)
			Quadruples.push_jump(-1)
		else: 
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else: 
		print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_updateQuadFor(t):
	'updateQuadFor : '
	# Update gotof quadruple when for finishes
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTO", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT'
	# Check if id exists in currentScope and set its value
	if t[1] in variableTable[currentScope]:
		temp_quad = Quadruple("=", t[3], '_', t[1])
		Quadruples.push_quad(temp_quad)
		variableTable[currentScope][t[1]]["value"] = t[3]
	# Check if id exists in global scope and set its value
	elif t[1] in variableTable["global"]:
		temp_quad = Quadruple("=", t[3], '_', t[1])
		Quadruples.push_quad(temp_quad)
		variableTable["global"][t[1]]["value"] = t[3]
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_vars(t):
	'vars : ID addVarsToTable varsArray varsComa'

def p_addVarsToTable(t):
	'addVarsToTable : '
	# If current ID (t[-1]) exists in scope or global, throw error
	if t[-1] in variableTable[currentScope]:
		print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		# Add current ID (t[-1]) to variableTable[scope]
		variableTable[currentScope][t[-1]] = {"type": currentType}

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''

def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix
				 | '''

def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK
				  | '''

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
	functionDir[currentScope]["varLength"] = Quadruples.func_quads
	Quadruples.func_quads = 0
	currentScope = "global"

def p_addFuncToDir(t):
	'addFuncToDir : '
	# If function exists in global scope, throw an error
	if t[-1] in variableTable["global"]:
		print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		global currentScope
		global currentType
		# Add function to variableTable of currentScope
		variableTable["global"][t[-1]] = {"type": currentType}
		# Change scope to new function id
		currentScope = t[-1]
		# Initialize variableTable and functionDir for new function id
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Set new function type and vars as reference to variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]

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
		print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		# Add function param to variableTable of currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
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

def p_addTypeFloat(t):
	'addTypeFloat : '
	types.push("float")

def p_addTypeChar(t):
	'addTypeChar : '
	types.push("char")

def p_hyperExpression(t):
	'''hyperExpression : superExpression evaluateHE opHyperExpression hyperExpressionNested
					   | superExpression opMatrix 
					   | superExpression evaluateHE'''

def p_hyperExpressionNested(t):
	'''hyperExpressionNested : superExpression evaluateHE opHyperExpression hyperExpressionNested
							 | superExpression evaluateHE'''

def p_evaluateHE(t):
	'evaluateHE : '
	global temp
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
			if resType == "int":
				result = 0
				lOp = int(lOp)
				rOp = int(rOp)
				if (lOp != 0 and lOp != 1) or (rOp != 0 and rOp != 1):
					print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
					exit(0)
				# Evaluate expression and push quadruple
				if oper == "|":
					result = lOp or rOp
				else: 
					result = lOp and rOp
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
				types.push(resType)
				temp += 1
			else:
				print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
				exit(0)

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
	global temp
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
				result = 0
				if oper == ">": 
					result = float(lOp) > float(rOp)
				if oper == "<": 
					result = float(lOp) < float(rOp)
				if oper == "<>": 
					result = float(lOp) != float(rOp)
				if oper == "==": 
					result = float(lOp) == float(rOp)
				result = int(result)
				# Generate quadruple for expression
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
				types.push(resType)
				temp += 1
			else:
				print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
				exit(0)

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
	global temp
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
			# Check result type and evaluate expression
			if resType != "error":
				result = 0
				if oper == "+": 
					result = float(lOp) + float(rOp)
				if oper == "-": 
					result = float(lOp) - float(rOp)
				if result % 1 == 0:
					result = int(result)
				# Generate quadruple for expression
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
				types.push(resType)
				temp += 1
			else:
				print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
				exit(0)

def p_expFunction(t):
	'''expFunction : PLUS addOperator exp
				   | MINUS addOperator exp '''

def p_term(t):
	'''term : factor evaluateFactor termFunction
			| factor evaluateFactor '''

def p_evaluateFactor(t):
	'evaluateFactor : '
	global temp
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
			# Check result type and evaluate expression
			if resType != "error":
				if oper == "*": 
					result = float(lOp) * float(rOp)
				if oper == "/": 
					result = float(lOp) / float(rOp)
				if result % 1 == 0:
					result = int(result)
				# Generate quadruple for expression
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
				types.push(resType)
				temp += 1
			else:
				print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
				exit(0)

def p_termFunction(t):
	'''termFunction : MULTIPLY addOperator term
					| DIVIDE addOperator term '''

def p_addOperator(t):
	'addOperator : '
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR hyperExpression RIGHTPAR
			  | cst_prim addOperandCst
			  | module
			  | ID addOperandId addTypeId'''

def p_addOperandCst(t):
	'addOperandCst : '
	operands.push(t[-1])

def p_addOperandId(t):
	'addOperandId : '
	# Add currentScope operand value to operand stack
	if t[-1] in variableTable[currentScope]:
		if "value" in variableTable[currentScope][t[-1]]:
			operands.push(variableTable[currentScope][t[-1]]["value"])
		else:
			print("Error: variable '%s' in line %d has not been assigned a value" %(t[-1], t.lexer.lineno))
			exit(0)
	# Add global scope operand value to operand stack
	elif t[-1] in variableTable["global"]:
		if "value" in variableTable["global"][t[-1]]:
			operands.push(variableTable["global"][t[-1]]["value"])
		else:
			print("Error: variable '%s' in line %d has not been assigned a value" %(t[-1], t.lexer.lineno))
			exit(0)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[-1], t.lexer.lineno))
		exit(0)

def p_addTypeId(t):
	'addTypeId : '
	# Push types to types stack
	if t[-2] in variableTable[currentScope]:
		types.push(variableTable[currentScope][t[-2]]["type"])
	elif t[-2] in variableTable["global"]:
		types.push(variableTable["global"][t[-2]]["type"])
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[-1], t.lexer.lineno))

def p_read(t):
	'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
	'id_list : ID addRead id_listFunction'

def p_addRead(t):
	'addRead : '
	# Generate read quadruple
	if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
		temp_quad = Quadruple("read", '_', '_', t[-1])
		Quadruples.push_quad(temp_quad)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[-1], t.lexer.lineno))

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

def p_print(t):
	'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_addPrint(t):
	'addPrint : '
	# Generate print quadruple
	temp_quad = Quadruple("print", '_', '_', operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()

def p_printFunction2(t):
	'printFunction2 : printFunction'

def p_print_param(t):
	'''print_param : hyperExpression addPrint
				   | CST_STRING addPrintString '''

def p_addPrintString(t):
	'addPrintString : '
	# Add string to print quadruple
	temp_quad = Quadruple("print", '_', '_', t[-1])
	Quadruples.push_quad(temp_quad)

def p_statement(t):
	'''statement : return
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module statement
				 | for statement
				 | while statement 
				 | '''

def p_module(t):
	'module : ID checkFuncExists genERASize LEFTPAR moduleFunction nullParam RIGHTPAR genGosub SEMICOLON'

def p_checkFuncExists(t):
	'checkFuncExists : '
	if t[-1] not in functionDir:
		print("Error: use of undefined module '%s' in line %d" % (t[-1], t.lexer.lineno))
		exit(0)
	global funcName
	funcName = t[-1]

def p_genERASize(t):
	'genERASize : '
	#Generate ERA size pending
	global funcName
	tmp_quad = Quadruple("ERA", funcName, "_", "_")
	Quadruples.push_quad(tmp_quad)
	global k
	k = 1

def p_nullParam(t):
	'nullParam : '
	global k
	global funcName
	if k < len(functionDir[funcName]["params"].values()):
		print("Error: unexpected number of arguments in module '%s' call in line %d." % (funcName, t.lexer.lineno))
		exit(0)

def p_genGosub(t):
	'genGosub : '
	tmp_quad = Quadruple("GOSUB", funcName, "_", functionDir[funcName]["start"])
	Quadruples.push_quad(tmp_quad)

def p_moduleFunction(t):
	'''moduleFunction : hyperExpression genParam nextParam COMA moduleFunction
					  | hyperExpression genParam 
					  | '''

def p_genParam(t):
	'genParam : '
	global k
	arg = operands.pop()
	argType = types.pop()
	paramList = functionDir[funcName]["params"].values()
	if k > len(paramList):
		print("Error: unexpected number of arguments in module '%s' call in line %d." % (funcName, t.lexer.lineno))
		exit(0)
	if argType == paramList[-k]:
		tmp_quad = Quadruple("PARAM", arg, '_', "param%d" % k)
		Quadruples.push_quad(tmp_quad)
	else:
		print("Error: type mismatch in module '%s' call in line %d." % (funcName, t.lexer.lineno))
		exit(0)

def p_nextParam(t):
	'nextParam : '
	global k
	k += 1

def p_error(t):
	print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))
	exit(0)

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)