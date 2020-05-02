from datastructures import *
import sys

class Quadruple(object):
	"""Quadruple class
	
	Quadrupe
	"""
	def __init__(self, operator, left_operand, right_operand, result):
		"""Build quadruple
		
		Build quadruple
		
		Arguments:
			operator {int} -- operator
			left_operand {operand} -- left operand
			right_operand {operand} -- right operand
			result {operand} -- result operand
		"""
		self.id = -1 # auto_incremented
		self.operator = operator
		self.left_operand = left_operand
		self.right_operand = right_operand
		self.result = result

	def print(self):
		print("Q"+ str(self.id), self.operator, self.left_operand, self.right_operand, self.result)


class Quadruples(object):
	"""Quadruples class
	
	Quadruple class manager
	"""
	# Class variables
	quadruples = []
	jump_stack = Stack()
	next_id = 0
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	# Quad Methods
	@classmethod
	def push_quad(cls, quad):
		"""Push quadruple
		
		Push quadruple to quadruple list
		
		Arguments:
			quad {Quadruple} -- Quadruple
		"""
		quad.id = cls.next_id
		cls.quadruples.append(quad)
		cls.next_id = len(cls.quadruples)

	@classmethod
	def pop_quad(cls):
		"""Pop quadruple
		
		Pop quadruple from quadruple list
		
		Returns:
			Quadruple -- Quadruple
		"""
		cls.next_id = len(cls.quadruples) - 1
		return cls.quadruples.pop()

	@classmethod
	def update_jump_quad(cls, quad_id, jump_id):
		"""update jump quad
		
		Add jump quadruple id (jump_id) to quadruple
		
		Arguments:
			quad_id {int} -- quadruple id
			jump_int {int} -- int
		"""
		cls.quadruples[quad_id].result = jump_id

	# Jump Stack Methods
	@classmethod
	def push_jump(cls, offset):
		"""Push jump
		
		Pushes the id of next free quad plus offset to the jump stack
		
		Arguments:
			offset {int} -- number
		"""
		cls.jump_stack.push(cls.next_id + offset)

	@classmethod
	def pop_jump(cls):
		"""Pop jump
		
		Pop the id of quadruple from jump stack
		
		Returns:
			int -- number
		"""
		return cls.jump_stack.pop()
		
	@classmethod
	def peek_jump(cls):
		"""Peek jump
		
		Peeks the id of jump quadruple
		
		Returns:
			int -- number
		"""
		return cls.jump_stack.peek()

	@classmethod
	def print_jump_stack(cls):
		"""print jump stack
		
		Prints the jump stack
		"""
		cls.jump_stack.pprint()

	@classmethod
	def print_all(cls):
		"""prints all quadruples from list """
		count = 0
		print("Quads ===============================")
		for x in cls.quadruples:
			x.print()