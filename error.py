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
	def operation_type_mismatch(lineno):
		" operation type mismatch error "
		print("Error: type mismatch in an operation in line %d." % (lineno))
		exit(0)

	@staticmethod
	def undefined_variable(t, lineno):
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
		print("Error: variable '%s' in line %d has not been assigned a value." % (t, lineno))
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
		print("Error: return statement on void function in line %d." % (lineno))
		exit(0)

	@staticmethod
	def no_return_on_function(t, lineno):
		print("Error: no return statement on function with return type in line %d." % (lineno))
		exit(0)

	@staticmethod
	def matrix_accessed_as_array(t, lineno):
		print("Error: matrix '%s' accessed as an array in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def type_mismatch_in_index(t, lineno):
		print("Error: type mismatch in variable '%s' indexation in line %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_matrix(t, lineno):
		print("Error: variable '%s' in line %d is not subscriptable as a matrix." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_array(t, lineno):
		print("Error: variable '%s' in line %d is not subscriptable as an array." % (t, lineno))
		exit(0)

	@staticmethod
	def array_parameter_in_module_call(lineno):
		print("Error: array parameter in module call in line %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_print_on_array_variable(lineno):
		print("Error: invalid print on array variable in line %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_operator_on_arrays(lineno):
		print("Error: invalid operator on arrays in line %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_operation_in_line(lineno):
		print("Error: invalid operation in line %d." % (lineno))
		exit(0)

	@staticmethod
	def dimensions_do_not_match(lineno):
		print("Error: operation between variables with dimensions that don't match in line %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_assignment_to_array_variable(lineno):
		print("Error: invalid assignment to array variable in line %d." % (lineno))
		exit(0)

	@staticmethod
	def array_size_must_be_positive(t, lineno):
		print("Error: array '%s' size in line %d must be positive." % (t, lineno))
		exit(0)

	@staticmethod
	def index_out_of_bounds():
		print("Error: index out of bounds.")
		exit(0)

	@staticmethod
	def invalid_determinant_calculation(lineno):
		print("Error: invalid array dimensions for determinant calculation in line %d." % (lineno))
		exit(0)

	@staticmethod
	def division_by_zero():
		print("Error: division by zero.")
		exit(0)

	@staticmethod
	def invalid_inverse_calculation(lineno):
		print("Error: invalid array dimensions for inverse calculation in line %d." % (lineno))
		exit(0)

	@staticmethod
	def type_mismatch_array_assignment(lineno):
		print("Error: type mismatch in array assignment in line %d." % (lineno))
		exit(0)
	
	@staticmethod
	def inverse_determinant_zero():
		print("Error: determinant of the inverse is zero.")
		exit(0)
		
	@staticmethod
	def type_mismatch_on_return(lineno):
		print("Error: type mismatch on return in line %d." % (lineno))
		exit(0)