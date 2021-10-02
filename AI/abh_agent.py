import random
from agent_interface import AgentInterface
from othello import OthelloState

square_weights = [
            120, -20,  20,   5,   5,  20, -20, 120,
            -20, -40,  -5,  -5,  -5,  -5, -40, -20,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            -20, -40,  -5,  -5,  -5,  -5, -40, -20,
            120, -20,  20,   5,   5,  20, -20, 120 ]
corners = dict()
corners[0] = [1,8,9]
corners[7] = [6,14,15]
corners[56] = [48,49,57]
corners[63] = [54,55,62]
neighbour_squares= [-9,-8,-7,-1,+1,+7,+8,+9]

class ABHAgent(AgentInterface):
	"""
	An agent who plays the Othello game using Minimax algorithm
	`info` returns the agent's information
	`decide` chooses an action from possible actions
	"""
	
	def __init__(self, weights):
		"""
		`depth` is the limit on the depth of Minimax tree
		"""
		self.weights = weights
		# print (self.weights)
	
	def info(self):
		return {"agent name": "ABH AKA THE RESHUFFLER",  # COMPLETE HERE
		"student name": ["Oliver Kalleinen"],  # COMPLETE HERE
		"student number": ["007"]}  # COMPLETE HERE
	
	def decide(self, state, actions):
		"""
		Get the value of each action by passing its successor to min_value
		function. Randomly choose from the actions with the maximum value.
		
		NOTE: `(values[action] - max_value > -1)` enforces choosing randomly
		from the actions with the exact maximum value. By replacing `-1` with
		`-k`, candidates with lower values can be considered too.
		
		"""
		global prunecount 
		prunecount = 0
		depth = 1
		while True:
			depth = depth + 1
			values = {}
			alpha = float('-inf')
			beta = float('inf')
			# player = state.player
			for action in actions:
				values[action] = self.min_value(state.successor(action), depth - 1, alpha, beta)
			max_value = max(values.values())
			candidates = [action for action in actions if (values[action] - max_value > -1)]
			selected_candidate = random.choice(candidates)
			# print()
			# print (depth)
			# print (max_value)
			# print (selected_candidate)
			# state.successor(action).printstate()
			# print()
			yield selected_candidate
	
	def max_value(self, state, depth, alpha, beta):
		"""
		Get the value of each action by passing its successor to min_value
		function. Return the maximum value of successors.
		
		`max_value` sees the game from players's perspective.
		
		NOTE: when passing the successor to min_value, `depth` must be
		reduced by 1, as we go down the Minimax tree. If `depth` is equal to
		zero or the game is finished (i.e., there are no applicable actions)
		then the number of root player's pieces is returned as the value.
		
		IMPORTANT NOTE: the player must check if it is the winner (or loser)
		of the game, in which case, a large value (or a negative value) must
		be assigned to the state. This is done by  checking if the previous turn
		has been a move or a pass. In case it has been a pass, i.e. 
		`(not state.previousMoved)`, an empty list of actions means the game
		must end. If the game continues, the depth must also be checked.
		
		"""
		global prunecount 
		actions = state.actions()
		if not actions:
			if (not state.previousMoved):
				if (state.count(state.player)>state.count(state.otherPlayer)):
					return 10000
				if (state.count(state.player)<state.count(state.otherPlayer)):
					return -10000
				return state.count(state.player)
			else:
				if not (depth == 0):
					return self.min_value(OthelloState(state), depth - 1, alpha, beta)
		if depth == 0:
			# return state.count(state.player)
			return self.heuristics(state, state.player, self.weights)
		value = float('-inf')
		for action in actions:
			value = max(value, self.min_value(state.successor(action), depth - 1, alpha, beta))
			alpha = max(value, alpha)
			if beta <= alpha:
				prunecount = prunecount + 1
				# print(f"NOT ORDERED tree pruned : {prunecount}")
				break
		return value
	
	def min_value(self, state, depth, alpha, beta):
		"""
		Get the value of each action by passing its successor to max_value
		function. Return the minimum value of successors.
		
		`min_value` sees the game from opponent's perspective, trying to
		minimize the value of next state.
		
		NOTE: when passing the successor to max_value, `depth` must be
		reduced by 1, as we go down the Minimax tree. If `depth` is equal to
		zero or the game is finished (i.e., there are no applicable actions)
		then the number of root players's pieces (i.e., 3 - state.player) is
		returned as the value.
	
		IMPORTANT NOTE: the opponent must check if it is the winner (or loser)
		of the game, in which case, a negative value (or a large value) must
		be assigned to the state. This is done by checking if the previous turn
		has been a move or a pass. In case it has been a pass, i.e. 
		`(not state.previousMoved)`, an empty list of actions means the game
		must end. If the game continues, the depth must also be checked.
		"""
		global prunecount 
		actions = state.actions()
		if not actions:
			if (not state.previousMoved):
				if (state.count(state.player)<state.count(state.otherPlayer)):
					return 10000
				if (state.count(state.player)>state.count(state.otherPlayer)):
					return -10000
				return state.count(3 -state.player)
			else:
				if not (depth == 0):
					return self.max_value(OthelloState(state), depth - 1, alpha, beta)
		if depth == 0:
			# return state.count(3 - state.player)
			return self.heuristics(state, state.otherPlayer(), self.weights)
		value = float('inf')
		for action in actions:
			value = min(value, self.max_value(state.successor(action), depth - 1, alpha, beta))
			beta = min(value, beta)
			if beta <= alpha:
				prunecount = prunecount + 1
				# print(f"NOT ORDERED tree pruned : {prunecount}")
				break
		return value
	
	
	#We could get a copy of the state like mobility, if the discs flip with any of the actions, then it is unstable, if not it is stable?
	
	
	
	def heuristics(self,state, player, weights):
		board = state.grid
		opponent = 3-player
		value_board = 0
		corner_count = 0
		corners_occupied = list()
		
		#Corners
		# update weights when corners are taken
		for corner in corners.keys():
			if board[corner] == player:
				corner_count += 1
				for square in corners[corner]:
					square_weights[square] = -1 * square_weights[square]
				corners_occupied.append(corner)
			elif board[corner] == opponent:
				corner_count -= 1
		for corner in corners_occupied:
			corners.pop(corner, None) # remove occupied corner
		
		#Control of the table
		for i in range(63):
			if board[i] == player:
				value_board += square_weights[i]
			elif board[i] == opponent:
				value_board -= square_weights[i]
		
		# check mobility
		possible_moves_player = list()
		possible_moves_opponent = list()
		mobility = 0
		possible_moves_player = state.actions()
		state_copy = OthelloState(state)
		possible_moves_opponent = state_copy.actions()
		mobility = len(possible_moves_player) - len(possible_moves_opponent)
		
		# check potential mobility
		potential_moves_player = 0
		potential_moves_opponent = 0
		potential_mobility = 0
		
		for i in range(9,55):
			if board[i] == 0:
				if i % 8 == 0: continue # discarding edges
				if i % 8 == 7: continue # discarding edges
				for square in neighbour_squares:
					if board[i+square] == opponent:
						potential_moves_player = potential_moves_player + 1
					elif board[i+square] == player:
						potential_moves_opponent = potential_moves_opponent + 1
		potential_mobility = potential_moves_player - potential_moves_opponent
		
		
		# add all values together
		heuristic = weights[0] * corner_count + weights[1]*value_board + weights[2] * mobility + weights[3] * potential_mobility
		return heuristic
	
