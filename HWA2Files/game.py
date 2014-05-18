import numpy as np
import random
#from enum import Enum

class Direction:
		left = 1
		right = 2
		up = 3
		down = 4
		
class Game(object):
	NUM_INIT = 2

	

	def __init__(self, size=4, testing=False):
		self.size = size
		self.score = 0
		self.max_block = 0
		self.won = False
		self.over = False
		self.num_moves = 0
		self.testing = testing

		self.state = np.zeros((self.size, self.size))

		if not self.testing:
			for i in range(Game.NUM_INIT):
				self.addRandom()

	def get(self, cell):
		if not self.within_bounds(cell):
			raise IndexError
		return self.state[cell['y']][cell['x']]

	def set(self, cell, value):
		if not self.within_bounds(cell):
			raise IndexError
		self.state[cell['y']][cell['x']] = value

	def move(self, direction):
		vec = None
		if direction == Direction.left:
			vec = {'x': -1, 'y': 0}
		elif direction == Direction.right:
			vec = {'x': 1, 'y': 0}
		elif direction == Direction.up:
			vec = {'x': 0, 'y': -1}
		elif direction == Direction.down:
			vec = {'x': 0, 'y': 1}
		else:
			raise 'Invalid Direction'

		traversals = self.build_traversals(vec)

		moved = False

		# print 'traversals', traversals

		for x in traversals['x']:
			for y in traversals['y']:
				cell = {'x': x, 'y': y}
				cell_value = self.get(cell)
				if cell_value > 0:
					positions = self.find_farthest_position(cell, vec)
					next = positions['next']
					farthest = positions['farthest']
					# print 'checking', cell, farthest, next
					valid = self.within_bounds(next)
					if valid:
						next_value = self.get(next)
					if valid and next_value == cell_value:
						# print 'merging', cell, next
						new_value = next_value * 2
						if new_value > self.max_block:
							self.max_block = new_value
						self.set(cell, 0)
						self.set(next, new_value)
						self.score += new_value
						if new_value == 2048:
							self.won = True
							self.over = True
						moved = True
						self.num_moves += 1

					elif not self.equal(cell, farthest):
						# print 'moving', cell, farthest
						self.set(cell, 0)
						self.set(farthest, cell_value)
						moved = True
						self.num_moves += 1

		if moved:
			if not self.testing:
				self.addRandom()

			if not self.is_moves_available():
				self.over = True
		return moved

	def is_moves_available(self):
		return self.is_available_cells() > 0 or self.is_merges_available()

	def is_merges_available(self):
		for x in range(self.size):
			for y in range(self.size):
				cell = {'x': x, 'y': y}
				cell_value = self.get(cell)
				right_cell = {'x': x + 1, 'y': y}
				if self.within_bounds(right_cell):
					right_cell_value = self.get(right_cell)
					if cell_value == right_cell_value:
						return True
				down_cell = {'x': x, 'y': y + 1}
				if self.within_bounds(down_cell):
					down_cell_value = self.get(down_cell)
					if cell_value == down_cell_value:
						return True
		return False

	def addRandom(self):
		available = self.get_available_cells()
		rand = random.choice(available)
		randValue = 2 if random.random() < 0.9 else 4
		# print 'setting', rand, randValue
		self.set(rand, randValue)

	def is_available_cells(self):
		for y in range(self.size):
			for x in range(self.size):
				cell_value = self.get({'x': x, 'y': y})
				if cell_value == 0:
					return True
		return False

	def get_available_cells(self):
		available = []
		for y in range(self.size):
			for x in range(self.size):
				cell = {'x': x, 'y': y}
				cellValue = self.get(cell)
				if cellValue == 0:
					available.append(cell)
		return available

	def equal(self, first, second):
		return first['x'] == second['x'] and first['y'] == second['y']


	def build_traversals(self, vec):
		traversals = {'x': [], 'y': []}
		for i in range(4):
			traversals['x'].append(i)
			traversals['y'].append(i)

		# Always traverse from the farthest cell in the chosen direction
		if vec['x'] == 1:
			traversals['x'].reverse()

		if vec['y'] == 1:
			traversals['y'].reverse()

		return traversals

	def find_farthest_position(self, cell, vec):
		previous = None
		while True:
			previous = cell
			cell = {'x': previous['x'] + vec['x'], 'y': previous['y'] + vec['y']}
			if not self.within_bounds(cell) or not self.cell_available(cell):
				break

		return {
		'farthest': previous,
		'next': cell
		}

	def within_bounds(self, cell):
		return 0 <= cell['x'] < self.size and 0 <= cell['y'] < self.size

	def cell_available(self, cell):
		return self.state[cell['y']][cell['x']] == 0

