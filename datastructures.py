
# Definition of Primitive Types
type_dict = {
	'int'	  	: 0,
	'float'		: 1,
	'char'	   	: 2,
}
inv_type_dict = {
	0: 			'int',
	1:			'float',
	2:			'char'
}

# Helper Classes
class Stack(object):
	"""Stack Class
	
	Stack class, using a list simulates a stack
	"""
	def __init__(self):
		self.values = []
	def isEmpty(self):
		return self.values == []
	def push(self,  value):
		self.values.append(value)
	def pop(self):
		if(len(self.values) > 0):
			return self.values.pop()
		else :
			print("Empty Stack")
	def peek(self):
		if(len(self.values) == 0):
			return None
		else:
			return self.values[len(self.values)-1]
	def size(self):
		return len(self.values)
	def pprint(self):
		print(self.values)
	def inStack(self, var_name):
		return var_name in self.values


class Queue(object):
	"""Queue Class
	
	Queue class, using a list simulates a queue
	"""

	def __init__(self):
		self.values = []
	def isEmpty(self):
		return self.values == []
	def enqueue(self, value):
		self.values.insert(0,value)
	def dequeue(self):
		if(len(self.values) > 0):
			return self.values.pop()
		else :
			print("Empty Queue")
	def peek(self):
		return self.values[len(self.values)-1]
	def size(self):
		return len(self.values)
	def pprint(self):
		print(self.values)
	def inQueue(self, var_name):
		return var_name in self.values
