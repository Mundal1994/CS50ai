"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
	"""
	Returns starting state of the board.
	"""
	return [[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY]]


def player(board):
	"""
	Returns player who has the next turn on a board.
	"""
	x = 0
	o = 0
	for row in board:
		for elem in row:
			if elem == X:
				x += 1
			elif elem == O:
				o += 1
	if o < x:
		return O
	return X


def actions(board):
	"""
	Returns set of all possible actions (i, j) available on the board.
	"""
	actions = []
	i = 0
	c = 0
	while i < 3:
		j = 0
		while j < 3:
			if board[i][j] == EMPTY:
				actions.append((i, j))
				c += 1
			j += 1
		i += 1
	return actions


def result(board, action):
	"""
	Returns the board that results from making move (i, j) on the board.
	"""
	i = 0
	new_board = list(map(list, board))
	while i < 3:
		j = 0
		while j < 3:
			if action[0] == i and action[1] == j:
				new_board[i][j] = player(board)
			j += 1
		i += 1
	return new_board


def winner(board):
	"""
	Returns the winner of the game, if there is one.
	"""
	count_x = 0
	count_o = 0
	i = 0
	check = X
	while i < 2:
		# horizontal check
		if board[0][0] == check and board[0][1] == check and board[0][2] == check:
			return check
		elif board[1][0] == check and board[1][1] == check and board[1][2] == check:
			return check
		elif board[2][0] == check and board[2][1] == check and board[2][2] == check:
			return check
		# vertical check
		elif board[0][0] == check and board[1][0] == check and board[2][0] == check:
			return check
		elif board[0][1] == check and board[1][1] == check and board[2][1] == check:
			return check
		elif board[0][2] == check and board[1][2] == check and board[2][2] == check:
			return check
		# diagonal check
		elif board[0][0] == check and board[1][1] == check and board[2][2] == check:
			return check
		elif board[0][2] == check and board[1][1] == check and board[2][0] == check:
			return check
		i += 1
		check = O
	return EMPTY


def terminal(board):
	"""
	Returns True if game is over, False otherwise.
	"""
	empty = 0
	if winner(board) == EMPTY:
		for row in board:
			for elem in row:
				if elem == EMPTY:
					empty += 1
		if empty == 0:
			return True
		return False
	return True


def utility(board):
	"""
	Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
	"""
	result = winner(board)
	if result == X:
		return 1
	elif result == O:
		return -1
	return 0


def minimax(board):
	"""
	Returns the optimal action for the current player on the board.
	"""
	if terminal(board) == True:
		return None
	current_player = player(board)
	moves = actions(board)
	i = 0
	move_len = len(moves)
	save_other_win = EMPTY
	middle = EMPTY
	# check if any of the moves can make any of the players win
	while i < move_len:
		# checks if current player can win
		if moves[i][0] == 1 and moves[i][1] == 1:
			middle = moves[i]
		temp_board = result(board, moves[i])
		current_player_win = winner(temp_board)
		if current_player_win == current_player:
			return moves[i]
		else:
			# checks if the other player can win
			k = 0
			new_board = list(map(list, board))
			while k < 3:
				j = 0
				while j < 3:
					if moves[i][0] == k and moves[i][1] == j:
						if current_player == X:
							new_board[k][j] = O
						else:
							new_board[k][j] = X
					j += 1
				k += 1
			other_player_win = winner(new_board)
			if other_player_win != EMPTY:
				save_other_win = moves[i]
		i += 1
	if save_other_win != EMPTY:
		return save_other_win
	# it will try to pick a free corner space to put its piece
	# if it's not the first piece it will choose the middle if it's free
	i = 0
	while i < move_len:
		if move_len < 8 and middle != EMPTY:
			return middle
		elif moves[i][0] == 0 and moves[i][1] == 0:
			return moves[i]
		elif moves[i][0] == 0 and moves[i][1] == 2:
			return moves[i]
		elif moves[i][0] == 2 and moves[i][1] == 0:
			return moves[i]
		elif moves[i][0] == 2 and moves[i][1] == 2:
			return moves[i]
		i += 1
	return moves[0]
