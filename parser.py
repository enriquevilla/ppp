import lexer as lexer
import ply.yacc as yacc
from datastructures import types, operands, operators, variableTable
from datastructures import functionDir, temp, currentScope, currentType, semanticCube
from quadruples import *

tokens = lexer.tokens

def p_program(t):
	'program : PROGRAM ID programA1 SEMICOLON programVars programFunc main'
	print("Code valid")
	# show variable table and function directory
	# print()
	# for i in functionDir:
	#	 print("\tfunction name: %s" % i)
	#	 print("\t\ttype: %s" % functionDir[i]["type"])
	#	 print("\t\tvars: %s" % functionDir[i]["vars"])
	#	 print()
	
	operands.print()
	types.print()
	operators.print()
	Quadruples.print_all()
	variableTable.clear()

# global scope varTable
def p_globalTable(t):
	'programA1 : '
	# Initialize variableTable for global and set program name and type
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Initialize functionDir for global scope
	functionDir[currentScope] = {}
	# Set type and vars as reference to variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_programVars(t):
	'''programVars : declaration
				   | '''

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

def p_main(t):
	'main : mainA1 MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

# main scope varTable
def p_mainTable(t):
	'mainA1 : '
	global currentScope
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
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.peek(), '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = operands.pop()
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
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
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : ELSE createJumpQuadElse LEFTBRACE statement RIGHTBRACE
			  | '''

def p_createJumpQuadElse(t):
	'createJumpQuadElse : '
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
	'while : WHILE LEFTPAR hyperExpression RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_for(t):
	'for : FOR forAssignment TO insertJumpFor hyperExpression createQuadFor LEFTBRACE statement RIGHTBRACE updateQuadFor'

def p_insertJumpFor(t):
	'insertJumpFor : '
	Quadruples.push_jump(0)

def p_createQuadFor(t):
	'createQuadFor : '
	result_type = types.pop()
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
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTO", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT cstprimA1'
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			temp_quad = Quadruple("=", t[3], '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = t[3]
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			temp_quad = Quadruple("=", t[3], '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable["global"][t[1]]["value"] = t[3]
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_vars(t):
	'vars : ID varsA1 varsArray varsComa'

# add vars to varTable
def p_addToTable(t):
	'varsA1 : '
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
	'''function : functionType ID functionA1 LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
				| functionType ID functionA1 LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''
	# When exiting function scope, reset scope to global and delete variableTable and reference to it in functionDir
	global currentScope
	# del variableTable[currentScope]
	# del functionDir[currentScope]["vars"]
	currentScope = "global"

# add function to dir
def p_addToDir(t):
	'functionA1 : '
	# If function exists in global scope, throw an error
	if t[-1] in functionDir["global"] or t[-1] in variableTable["global"]:
		print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		global currentScope
		global currentType
		# Add function to variableTable of currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
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
					| FUNCTION VOID functionTypeA1'''

# set void as current type
def p_setVoid(t):
	'functionTypeA1 : '
	# Set void as currentType
	global currentType
	currentType = t[-1]

def p_param(t):
	'param : primitive ID paramA1 functionParam'

# add function params to table
def p_addFuncParams(t):
	'paramA1 : '
	# If function param exists in scope or globally, throw error
	if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
		print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		# Add function param to variableTable of currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

def p_cst_prim(t):
	'''cst_prim : CST_INT cstprimA1
				| CST_FLOAT cstprimA2
				| CST_CHAR cstprimA3'''
	t[0] = t[1]

# add type int
def p_addTypeI(t):
	'cstprimA1 : '
	types.push("int")

# add type float
def p_addTypeF(t):
	'cstprimA2 : '
	types.push("float")

# add type char
def p_addTypeC(t):
	'cstprimA3 : '
	types.push("char")

def p_hyperExpression(t):
	'''hyperExpression : superExpression hyperExpA1 opHyperExpression hyperExpressionNested
					   | superExpression opMatrix 
					   | superExpression hyperExpA1'''

def p_hyperExpressionNested(t):
	'''hyperExpressionNested : superExpression hyperExpA1 opHyperExpression hyperExpressionNested
							 | superExpression hyperExpA1'''

def p_opConsumeHyperExp(t):
	'hyperExpA1 : '
	global temp
	if operators.size() != 0:
		if operators.peek() == "|" or operators.peek() == "&":
			rOp = operands.pop()
			lOp = operands.pop()
			oper = operators.pop()
			rType = types.pop()
			lType = types.pop()
			resType = semanticCube[(lType, rType, oper)]
			if resType == "int":
				result = 0
				lOp = int(lOp)
				rOp = int(rOp)
				if (lOp != 0 and lOp != 1) or (rOp != 0 and rOp != 1):
					print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
					exit(0)
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
	'''superExpression : exp superExpA1 opSuperExpression exp superExpA1
					   | exp superExpA1 '''

def p_opConsumeSuperExp(t):
	'superExpA1 : '
	global temp
	if operators.size() != 0:
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==":
			rOp = operands.pop()
			lOp = operands.pop()
			oper = operators.pop()
			rType = types.pop()
			lType = types.pop()
			resType = semanticCube[(lType, rType, oper)]
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
	'''exp : term termA1 expFunction
		   | term termA1 '''

def p_opConsumeExp(t):
	'termA1 : '
	global temp
	if operators.size() != 0:
		if operators.peek() == "+" or operators.peek() == "-":
			rOp = operands.pop()
			lOp = operands.pop()
			oper = operators.pop()
			rType = types.pop()
			lType = types.pop()
			resType = semanticCube[(lType, rType, oper)]
			if resType != "error":
				result = 0
				if oper == "+": 
					result = float(lOp) + float(rOp)
				if oper == "-": 
					result = float(lOp) - float(rOp)
				if result % 1 == 0:
					result = int(result)
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
	'''term : factor factorA1 termFunction
			| factor factorA1 '''

def p_opConsumeTerm(t):
	'factorA1 : '
	global temp
	if operators.size() != 0:
		if operators.peek() == "*" or operators.peek() == "/":
			rOp = operands.pop()
			lOp = operands.pop()
			oper = operators.pop()
			rType = types.pop()
			lType = types.pop()
			resType = semanticCube[(lType, rType, oper)]
			if resType != "error":
				if oper == "*": 
					result = float(lOp) * float(rOp)
				if oper == "/": 
					result = float(lOp) / float(rOp)
				if result % 1 == 0:
					result = int(result)
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
	if t[-1] in variableTable[currentScope]:
		if "value" in variableTable[currentScope][t[-1]]:
			operands.push(variableTable[currentScope][t[-1]]["value"])
		else:
			print("Error: variable '%s' in line %d has not been assigned a value" %(t[-1], t.lexer.lineno))
			exit(0)
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
	temp_quad = Quadruple("print", '_', '_', t[-1])
	Quadruples.push_quad(temp_quad)

def p_statement(t):
	'''statement : return
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | declaration statement
				 | module statement
				 | for statement
				 | while statement 
				 | '''

def p_module(t):
	'module : ID LEFTPAR moduleFunction RIGHTPAR SEMICOLON'

def p_moduleFunction(t):
	'''moduleFunction : hyperExpression COMA moduleFunction
					  | hyperExpression RIGHTPAR
					  | '''

def p_error(t):
	print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))
	exit(0)

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)