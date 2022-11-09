import itertools
import random


class Minesweeper():
	"""
	Minesweeper game representation
	"""

	def __init__(self, height=8, width=8, mines=8):

		# Set initial width, height, and number of mines
		self.height = height
		self.width = width
		self.mines = set()

		# Initialize an empty field with no mines
		self.board = []
		for i in range(self.height):
			row = []
			for j in range(self.width):
				row.append(False)
			self.board.append(row)

		# Add mines randomly
		while len(self.mines) != mines:
			i = random.randrange(height)
			j = random.randrange(width)
			if not self.board[i][j]:
				self.mines.add((i, j))
				self.board[i][j] = True

		# At first, player has found no mines
		self.mines_found = set()

	def print(self):
		"""
		Prints a text-based representation
		of where mines are located.
		"""
		for i in range(self.height):
			print("--" * self.width + "-")
			for j in range(self.width):
				if self.board[i][j]:
					print("|X", end="")
				else:
					print("| ", end="")
			print("|")
		print("--" * self.width + "-")

	def is_mine(self, cell):
		i, j = cell
		return self.board[i][j]

	def nearby_mines(self, cell):
		"""
		Returns the number of mines that are
		within one row and column of a given cell,
		not including the cell itself.
		"""

		# Keep count of nearby mines
		count = 0

		# Loop over all cells within one row and column
		for i in range(cell[0] - 1, cell[0] + 2):
			for j in range(cell[1] - 1, cell[1] + 2):

				# Ignore the cell itself
				if (i, j) == cell:
					continue

				# Update count if cell in bounds and is mine
				if 0 <= i < self.height and 0 <= j < self.width:
					if self.board[i][j]:
						count += 1

		return count

	def won(self):
		"""
		Checks if all mines have been flagged.
		"""
		return self.mines_found == self.mines


class Sentence():
	"""
	Logical statement about a Minesweeper game
	A sentence consists of a set of board cells,
	and a count of the number of those cells which are mines.
	"""

	def __init__(self, cells, count):
		self.cells = set(cells)
		self.count = count

	def __eq__(self, other):
		return self.cells == other.cells and self.count == other.count

	def __str__(self):
		return f"{self.cells} = {self.count}"

	def known_mines(self):
		"""
		Returns the set of all cells in self.cells known to be mines.
		"""
		if len(self.cells) == self.count:
			return self.cells
		return None

	def known_safes(self):
		"""
		Returns the set of all cells in self.cells known to be safe.
		"""
		if self.count == 0:
			return self.cells
		return None

	def mark_mine(self, cell):
		"""
		Updates internal knowledge representation given the fact that
		a cell is known to be a mine.
		"""
		if cell in self.cells and self.known_mines() == None:
			self.cells.discard(cell)
			self.count -= 1


	def mark_safe(self, cell):
		"""
		Updates internal knowledge representation given the fact that
		a cell is known to be safe.
		"""
		if cell in self.cells and self.known_safes() == None:
			self.cells.discard(cell)


class MinesweeperAI():
	"""
	Minesweeper game player
	"""

	def __init__(self, height=8, width=8):

		# Set initial height and width
		self.height = height
		self.width = width

		# Keep track of which cells have been clicked on
		self.moves_made = set()

		# Keep track of cells known to be safe or mines
		self.mines = set()
		self.safes = set()

		# List of sentences about the game known to be true
		self.knowledge = []

	def mark_mine(self, cell):
		"""
		Marks a cell as a mine, and updates all knowledge
		to mark that cell as a mine as well.
		"""
		self.mines.add(cell)
		for sentence in self.knowledge:
			sentence.mark_mine(cell)

	def mark_safe(self, cell):
		"""
		Marks a cell as safe, and updates all knowledge
		to mark that cell as safe as well.
		"""
		self.safes.add(cell)
		for sentence in self.knowledge:
			sentence.mark_safe(cell)

	def add_knowledge(self, cell, count):
		"""
		Called when the Minesweeper board tells us, for a given
		safe cell, how many neighboring cells have mines in them.

		This function should:
			1) mark the cell as a move that has been made
			2) mark the cell as safe
			3) add a new sentence to the AI's knowledge base
			   based on the value of `cell` and `count`
			4) mark any additional cells as safe or as mines
			   if it can be concluded based on the AI's knowledge base
			5) add any new sentences to the AI's knowledge base
			   if they can be inferred from existing knowledge
		"""
		self.mark_safe(cell)
		self.moves_made.add((cell))
		temp = Sentence((), count)
		# loop over all cells to figure out to construct sentence
		i = cell[0] - 1
		j_start = cell[1] - 1
		i_stop = cell[0] + 2
		j_stop = cell[1] + 2
		if i < 0:
			i = 0
		if j_start < 0:
			j_start = 0
		if i_stop > self.height:
			i_stop = self.height
		if j_stop > self.width:
			j_stop = self.width
		while i < i_stop:
			j = j_start
			while j < j_stop:
				found = 1
				# don't add to set if cell has already been marked as 'safe'
				for elem in self.moves_made:
					if elem == (i, j):
						found = 0
				for elem in self.safes:
					if elem == (i, j):
						found = 0
				if found == 1:
					temp.cells.add((i, j))
				j += 1
			i += 1
		if count == 0:
			# we know all of the cells are safe
			for elem in temp.cells:
				self.mark_safe(elem)
		elif len(temp.cells) == count:
			# we know all of the collected cells are mines
			for elem in temp.cells:
				self.mark_mine(elem)
		else:
			# if neither we will add the sentence to logic
			self.knowledge.append(temp)
		# loop through sentences in knowledge to see if we can add cells to either 'safe' or 'mine'
		for sentence in self.knowledge:
			# removes safe cells if we already have determed the remaining cells to be mines in the sentence
			if len(sentence.cells) > sentence.count and sentence.count > 0:
				temp = set()
				for elem in sentence.cells:
					for cell in self.mines:
						if elem == cell:
							temp.add(cell)
				if len(temp) > 0 and len(temp) == sentence.count:
					i = 0
					while i == 0:
						for elem in sentence.cells:
							found = 0
							for cell in temp:
								if elem == cell:
									found = 1
							if found == 0:
								self.mark_safe(elem)
								break
						if found == 1:
							break
			# makes sure cells that has a count equal to 0 is marked as 'safe'
			if len(sentence.cells) > 0 and sentence.count == 0:
				for elem in sentence.cells:
					self.mark_safe(elem)
			# makes sure cells that has a len count equal equal to count is marked as 'mines'
			elif len(sentence.cells) == sentence.count and sentence.count > 0:
				for elem in sentence.cells:
					self.mark_mine(elem)

	def make_safe_move(self):
		"""
		Returns a safe cell to choose on the Minesweeper board.
		The move must be known to be safe, and not already a move
		that has been made.

		This function may use the knowledge in self.mines, self.safes
		and self.moves_made, but should not modify any of those values.
		"""
		# calculate how many safe moves are remaining
		remain = self.safes - self.moves_made
		if len(remain) != 0:
			# select random index and loops through all elements of remain
			# when reaching the random index the current element will be returned
			random_index = random.choice(range(0, len(remain)))
			i = 0
			for elem in remain:
				if i == random_index:
					return (elem)
				i += 1
		return None

	def make_random_move(self):
		"""
		Returns a move to make on the Minesweeper board.
		Should choose randomly among cells that:
			1) have not already been chosen, and
			2) are not known to be mines
		"""
		# start with collecting all of the moves that are neither
		# a mine nor a move that has already been made
		remain = set()
		# try to collect information from sentences in knowledge and choose the ones
		# that contains the most safe cells
		for sentence in self.knowledge:
			if sentence.count > 0 and len(sentence.cells) - sentence.count >= 3:
				for elem in sentence.cells:
					found = 0
					for cell in self.mines:
						found = 1
					if found == 0:
						remain.add(elem)
		# collect all cells on board that has not already been moved nor known to be mines
		if len(remain) < 10:
			for i in range(self.height):
				for j in range(self.width):
					found = 0
					for elem in self.mines:
						if elem == (i, j):
							found = 1
					for elem in self.moves_made:
						if elem == (i, j):
							found = 1
					if found == 0:
						remain.add((i, j))
		# if elements have been collected a random index will be choosen
		# and we will loop over each element in 'remain' and return the
		# element that is present at random_index
		if len(remain) != 0:
			random_index = random.choice(range(0, len(remain)))
			i = 0
			for elem in remain:
				if i == random_index:
					return (elem)
				i += 1
		return None
