import sys

class Error:
	""" Error class
	
		Static class to centralize error displays.
	"""
	@staticmethod
	def syntax(t, lineno):
		" syntax error "
		print("Syntax error: Unexpected token '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def type_mismatch(t, lineno):
		" type mismatch error "
		print("Error: type mismatch in assignment for '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def condition_type_mismatch(lineno):
		"if expression type mismatch error"
		print("Error: type mismatch in condition expression in line %d." % lineno)
		exit(0)
		
	@staticmethod
	def operation_type_mismatch(lOp, rOp, lineno):
		" operation type mismatch error "
		print("Error: type mismatch between '%s' and '%s' in line %d." % (lOp, rOp, lineno))
		exit(0)
	
	@staticmethod
	def undefined_variable(t,lineno):
		" use of undeclared variable error "
		print("Error: use of undefined variable '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_variable(t, lineno):
		" variable redefinition error "
		print("Error: redefinition of variable '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_has_no_assigned_value(t, lineno):
		" variable no assigned value error "
		print("Error: variable '%s' in line %d has not been assigned a value." %(t, lineno))
		exit(0)

	@staticmethod
	def undefined_module(t, lineno):
		" undefined module error "
		print("Error: use of undefined module '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def unexpected_number_of_arguments(t, lineno):
		" wrong number of arguments error"
		print("Error: unexpected number of arguments in module '%s' call in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def type_mismatch_module(t, lineno):
		print("Error: type mismatch in module '%s' call in line %d." % (t, lineno))
		exit(0)
	
	@staticmethod
	def return_on_void_function(t, lineno):
		print("Error: return statement on void function. Line: %d." % (lineno))
		exit(0)

	@staticmethod
	def no_return_on_function(t, lineno):
		print("Error: no return statement on function with return type. Line: %d." % (lineno))
		exit(0)