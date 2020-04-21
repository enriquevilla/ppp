# Semantic Controller

#include datastructures for Stack, Queue and variable types.
from datastructures import *
import sys

# DEFINE CLASSES
class Var:
	"""Var Class
	
	Used to construct variables by the compiler

    Attributes {
        id: unique identifier for each object
        name: how the variable is instanciated
        type: variable type
        value: value assigned to the variable
    }
	"""
	# Instance
	def __init__(self):
		self.id = -1
		self.name = ""
		self.type = 0
		self.value = None

	def erase(self):
		self.id = -1
		self.name = ""
		self.type = 0
		self.value = None

	def init_var(self, id, name, type, value):
		self.id = id
		self.name = name
		self.type = type
		self.value = value

	def print_var(self):
		print "\t\tid: " + str(self.id) + ",\n\t\tname: " + self.name  + ",\n\t\ttype: " + str(self.type) + ",\n\t\tvalue: " + str(self.value)
		print "\t\t---------"

class Array:
	"""Array Class
	
	Class used to build an array by compiler
    Attributes {
        id: unique identifier for each object
        name: how the variable is instanciated
        type: variable type
        length: assigned length to the array
    }
	"""

	def __init__(self):
		self.id = -1
		self.name = ""
		self.type = 0
		self.length = 0

 	#initialize when length is unknown
 	def init_arr(self, id, name, type, length):
 		self.id = id
		self.name = name
		self.type = type
		self.length = length

 	def print_arr(self):
 		print "\t\tARRAY! \n\t\tid: " + str(self.id) + ",\n\t\tname: " + self.name  + ",\n\t\ttype: " + str(self.type) + ",\n\t\tlength: " + str(self.length)

 	#to be able to print all
 	def print_var(self):
 		self.print_arr()


class Function:
	"""Function Class
	
	Class to build functions by compiler
    Attributes {
        id: Unique identifier for functions in program
        name: Function name to use when instanciating and using
        type: Value type of return
        vars: Dictionary of variables created when compiling
        has_return: whether the function uses return statements to finish running.
    }
	"""
	def __init__(self):
		self.id = -1
		self.name = ""
		self.type = 0
		self.vars = {}
		self.params = []
		self.quad_index = -1
		self.has_return = False

	def erase(self):
		self.id = -1
		self.name = ""
		self.type = 0 
		self.vars = {}
		self.params = []
		self.quad_index = -1
		self.has_return = False

	def init_func(self, id, name, type, q_index):
		self.id = id
		self.name = name
		self.type = type
		self.quad_index = q_index
		self.has_return = False

	def add_var(self, var):
		"""Add Var
		
		Adds a variable to the function's variable dictionary
		
		Arguments:
			var {Var} -- Var object
		"""
		if var.name not in self.vars:
			tmp_var = Var()
			tmp_var.init_var(None, var.name, var.type, var.value)
            
            # Fetches the corresponding ID to assign to this variable
			if self.name == 'program':
				tmp_var.id = SemanticInfo.get_next_global_var_id(var.type)
			else:
				tmp_var.id = SemanticInfo.get_next_var_id(var.type)

			self.vars[var.name] = tmp_var
			return tmp_var
		else:
			Error.already_defined('variable', var.name)


	def add_arr(self, arr):
		"""Add Array
		
		Adds an array to the function's variable dictionary
		
		Arguments:
			arr {Array} -- Array object
		
		Returns:
			Array -- Array object
		"""
		if arr.name not in self.vars:
			tmp_arr = Array()
			tmp_arr.init_arr(None, arr.name, arr.type, arr.length)
			
			# Fetches the corresponding ID to assign to this variable
			if self.name == 'program':
				tmp_arr.id = SemanticInfo.get_next_global_var_id(arr.type)
			else:
				tmp_arr.id = SemanticInfo.get_next_var_id(arr.type)

			self.vars[arr.name] = tmp_arr
			return tmp_arr
		else:
			Error.already_defined('variable array', arr.name)

class FunctionTable:
	"""Function table
	
	Function table
	"""

    #Begins with program function
	global_func = Function()
	global_func.init_func(0, 'program', type_dict['void'], None)
	
	function_dict = {
		'program' : global_func
	}

	constant_dict = {}

	next_func_id = 1
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	@classmethod
	def add_function(cls, func):
		"""Add Function
		
		Add function to function table
		
		Arguments:
			func {Func} -- function
		"""
		if func.name not in cls.function_dict:
			tmp_func = Function()
			tmp_func.init_func(cls.next_func_id, func.name, func.type, func.quad_index)
			cls.function_dict[func.name] = tmp_func
			cls.next_func_id += 1
		else:
			Error.already_defined('function', func.name)

	@classmethod
	def add_return_type_to_func(cls, name, type):
		""" add return type to function """
		cls.function_dict[name].type = type
		# Here we add a global var with the name of the func to make return
		# values easier to handle
		tmp_var = Var()
		tmp_var.init_var(-1, name, type, None)
		cls.function_dict['program'].add_var(tmp_var)

	@classmethod
	def add_var_quantities_to_func(cls, function_name):
		"""add variable to function
		
		Add variable to function
		
		Arguments:
			function_name {String} -- Name
		"""
		if function_name == 'program':
			var_qs = SemanticInfo.current_global_var_id
		else:
			var_qs = SemanticInfo.current_var_id

		q = [(x%1000) for x in var_qs]
		print "> Var q's for func '{}': {}".format(function_name, q)
		cls.function_dict[function_name].var_quantities = q

	@classmethod
	def print_all(cls):
		"""print all functions"""
		for x in cls.function_dict:
			print (x + ":")
			cls.function_dict[x].print_all()

	@classmethod
	def add_var_to_func(cls, function_name, var_obj):
		"""Adds variable to function
		
		Adds variable to function
		
		Arguments:
			function_name {string} -- function name
			var_obj {Var} -- variable object
		
		Returns:
			Var -- Variable
		"""
		# cls.function_dict[function_name].var_quantities[var_obj.type] += 1
		return cls.function_dict[function_name].add_var(var_obj)

	@classmethod
	def verify_var_in_func(cls, function_name, var_name):
		"""variable in function
		
		Verifies if variable is in function
		
		Arguments:
			function_name {string} -- function name
			var_name {string} -- variable name
		
		Returns:
			Bool -- bool
		"""
		return cls.function_dict[function_name].var_in_func(var_name) or cls.verify_var_global(var_name)

	@classmethod
	def add_param_to_func(cls, function_name, param_name, param_var):
		"""add parameter to function
		
		Adds parameter to function
		
		Arguments:
			function_name {string} -- func name
			param_name {string} -- param name
			param_var {Variable} -- param variable
		"""
		cls.function_dict[function_name].params.append((param_name, param_var.type, param_var.id))

	@classmethod
	def verify_var_global(cls, var_name):
		"""Verify if variable is global
		
		Verify if variable is in the global scope
		
		Arguments:
			var_name {string} -- variable name
		
		Returns:
			Bool -- bool
		"""
		return cls.function_dict["program"].var_in_func(var_name)

	@classmethod
	def get_var_in_scope(cls, p, function_name, var_name):
		"""get variable in scope
		
		Return variable from function scope
		
		Arguments:
			p {p} -- p
			function_name {string} -- string
			var_name {string} -- string
		
		Returns:
			Var -- Variable object
		"""
		if not cls.verify_var_in_func(function_name, var_name): # TODO: Double check from syntax, unecessary
			Error.variable_not_defined(var_name, p.lexer.lineno)
		try:
			var = cls.function_dict[function_name].vars[var_name]
		except KeyError:
			var = cls.function_dict["program"].vars[var_name]
		return var

	@classmethod
	def verify_param_at_index(cls, function_name, param_name, param_type, index):
		"""Verify parameter at index
		
		Verify parameter at selected index in the array
		
		Arguments:
			function_name {string} -- function name
			param_name {name} -- param name
			param_type {type} -- parameter type
			index {int} -- index number
		
		Returns:
			bool -- bool
		"""
		func = cls.function_dict[function_name]
		if index >= len(func.params):
			return False
		param_tuple = func.params[index]
		return (param_tuple[0] == param_name and param_tuple[1] == param_type)

	@classmethod
	def add_arr_to_func(cls, function_name, arr_obj):
		"""adds array to function
		
		Adds an array to the functions
		
		Arguments:
			function_name {string} -- function name
			arr_obj {Array} -- array instance
		
		Returns:
			Array -- Array object
		"""
		return cls.function_dict[function_name].add_arr(arr_obj)

	@classmethod
	def function_returns_void(cls, function_name):
		"""function returns if void
		
		returns if function is void
		
		Arguments:
			function_name {string} -- func name
		
		Returns:
			bool -- bool
		"""
		return cls.function_dict[function_name].function_is_void()

	@classmethod
	def set_return_found(cls, function_name, type):
		"""Set return found
		
		Set if return type is found
		
		Arguments:
			function_name {string} -- function name
			type {type} -- type
		"""
		cls.function_dict[function_name].set_has_Return(type)

	@classmethod
	def function_has_return_stmt(cls, function_name):
		"""Function has return statement
		
		Returns if function has a return statement 
		
		Arguments:
			function_name {string} -- function name
		
		Returns:
			Bool -- bool
		"""
		return cls.function_dict[function_name].get_has_Return()

	@classmethod
	def flipped_constant_dict(cls):
		"""Gets fliped constant dictionary
		
		Gets flipped constant dictionary
		"""
		return {v: k for k, v in cls.constant_dict.items()}
