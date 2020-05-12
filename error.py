import sys

class Error:
	""" Error class
	
		Static class to centralize error displays.
	"""
	@staticmethod
	def type_mismatch(t, lineno):
		"""type mismatch error """
		print("Error: type mismatch in assignment for '%s' in line %d" % (t, lineno))
		exit()
		
	@staticmethod
	def operation_type_mismatch(lOp, rOp, lineno):
		"""operation type mismatch error """
		print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, lineno))
		exit(0)
	
	@staticmethod
	def undeclared_variable(t,lineno):
		""" use of undeclared variable error """
		print("Error: use of undefined variable '%s' in line %d" % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_variable(t, lineno):
		print("Error: redefinition of variable '%s' in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_has_no_assigned_value(t, lineno):
		print("Error: variable '%s' in line %d has not been assigned a value" %(t, lineno))
		exit(0)

		