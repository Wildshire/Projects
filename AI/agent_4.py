import random
from othello import OthelloState
from agent_interface import AgentInterface


class Agent4(AgentInterface):
	"""
	An agent who plays the Othello game
	
	Methods
	-------
	`info` returns the agent's information
	`decide` chooses an action from possible actions
	"""
	
	@staticmethod
	def info():
		"""
		Return the agent's information
	
		Returns
		-------
		Dict[str, str]
			`agent name` is the agent's name
			`student name` is the list team members' names
			`student number` is the list of student numbers of the team members
		"""
		# -------- Task 1 -------------------------
		# Please complete the following information
	
		return {"agent name": "jgl2000_4",  # COMPLETE HERE
				"student name": ["Jose Gonzalez Lopez"],  # COMPLETE HERE
				"student number": ["893699"]}  # COMPLETE HERE
	
	def decide(self, state: OthelloState, actions: list):
		"""
		Generate a sequence of increasingly preferable actions
	
		Given the current `state` and all possible `actions`, this function
		should choose the action that leads to the agent's
		victory.
		However, since there is a time limit for the execution of this function,
		it is possible to choose a sequence of increasing preferable actions.
		Therefore, this function is designed as a generator; it means it should
		have no return statement, but it should `yield` a sequence of increasing
		good actions.
	
		IMPORTANT: If no action is yielded within the time limit, the game will
		choose a random action for the player.
	
		Parameters
		----------
		state: OthelloState
			Current state of the board
		actions: list
			List of all possible actions
	
		Yields
		------
		action
			the chosen `action`
		"""
		# -------- TASK 2 ------------------------------------------------------
		# Your task is to implement an algorithm to choose an action form the
		# given `actions` list. You can implement any algorithm you want.
		# However, you should keep in mind that the execution time of this
		# function is limited. So, instead of choosing just one action, you can
		# generate a sequence of increasing good action.
		# This function is a generator. So, you should use `yield` statement
		# rather than `return` statement. To find more information about
		# generator functions, you can take a look at:
		# https://www.geeksforgeeks.org/generators-in-python/
		#
		# If you generate multiple actions, the last action will be used in the
		# game.
		#
		# Tips
		# ====
		# 1. During development of your algorithm, you may want to find the next
		#    state after applying an action to the current state; in this case,
		#    you can use the following patterns:
		#    `next_state = current_state.successor(action)`
		#
		# 2. If you need to simulate a game from a specific state to find the
		#    the winner, you can use the following pattern:
		#    ```
		#    simulator = Game(FirstAgent(), SecondAgent())
		#    winner = simulator.play(starting_state=specified_state)
		#    ```
		#    The `MarkovAgent` has illustrated a concrete example of this
		#    pattern.
		#
		# 3. You are free to choose what kind of game-playing agent you
		#    implement. Some of the obvious approaches are the following:
		# 3.1 Implement alpha-beta (and investigate its potential for searching deeper
		#     than what is possible with Minimax). Also, the order in which the actions
		#     are tried in a given node impacts the effectiveness of alpha-beta: you could
		#     investigate different ways of ordering the actions/successor states.
		# 3.2 Try out better heuristics, e.g. ones that take into account the higher
		#     importance of edge and corner cells. Find material on this in the Internet.
		# 3.3 You could try out more advanced Monte Carlo search methods (however, we do
		#     not know whether MCTS is competitive because of the high cost of the full
		#     gameplays.)
		# 3.4 You could of course try something completely different if you are willing to
		#     invest more time.
		#
		# GL HF :)
		# ----------------------------------------------------------------------
	
		# Replace the following lines with your algorithm
		
		#Idea: make a score out of 100 point for each category and sum them up get action with highest score. Categories are: coin parity, stability, mobility, corners, control over edges. Also think about the idea of weighting each of them depending on the game. 	
		
		depth=4
		alpha=float("-inf") #Try to get a high as possible
		beta=float("inf") #Try to get as low as possible
		
		#sort actions
		actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
		max_value=-10000
		choice=None
		
		#Yielding choices until we ran out of time
		for action in actions:
			new_value = self.min_value(state.successor(action), depth - 1,alpha,beta)
			if(new_value>max_value):
				max_value=new_value
				choice=action
				yield choice
		
	#Maximizing node
	def max_value(self, state, depth,alpha,beta):
		actions = state.actions()
		if not actions:
			if (not state.previousMoved):
				if (state.count(state.player)>state.count(state.otherPlayer())):
					return 10000
				if (state.count(state.player)<state.count(state.otherPlayer())):
					return -10000
				return state.count(state.player)
			else:
				if not (depth == 0):
					return self.min_value(OthelloState(state), depth - 1,alpha,beta)
		#End of the search, my heuristic function
		if(depth==0):
			return self.heuristics(state,state.player)
	
		#Sort actions
		actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
		#Pruning
		i=0
		stop=False
		value = float('-inf')
		while(not stop and i<len(actions)):
			value = max(value,self.min_value(state.successor(actions[i]), depth - 1,alpha,beta))
			alpha = max(value, alpha)
			if alpha >= beta:
				stop=True
				continue
			i+=1	
		return value
		
	#Minimizing node	
	def min_value(self, state, depth,alpha,beta):
		actions = state.actions()
		if not actions:
			if (not state.previousMoved):
				if (state.count(state.player)<state.count(state.otherPlayer())):
					return 10000
				if (state.count(state.player)>state.count(state.otherPlayer())):
					return -10000
				return state.count(3 -state.player)
			else:
				if not (depth == 0):
					return self.max_value(OthelloState(state), depth - 1,alpha,beta)
		#End of the search, my heuristic function
		if(depth==0):
			return self.heuristics(state,state.otherPlayer())
		
		#Sort actions
		actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
		#Pruning
		i=0
		stop=False
		value = float('inf')
		while(not stop and i<len(actions)):
			value = min(value,self.max_value(state.successor(actions[i]), depth - 1,alpha,beta))
			beta = min(value,beta)
			if(beta<=alpha):
				stop=True
				continue
			i+=1	
		return value
		
	
	#My heuristic function
	def heuristics(self,state,player):
		opponent=3-player
		
		#Get corners indicator
		final_corners=self.corners(state,player,opponent)
		
		#Get control of the table
		final_control=self.control_over_table(state,player,opponent,self.get_weights())		
		
		#Get mobility
		final_mobility=self.mobility(state,player,opponent)
		
		#Get frontier
		final_frontier=self.frontier(state,player,opponent)
		
		#Get stability if at least one corner is occupied
		final_stability=0
		if(final_corners!=0):
			final_stability=self.stability(state,player,opponent)
		
		return final_corners+final_control+final_mobility+final_stability
	
	#Functions for calculating the heuristic   
	#Corners
	def corners(self,state,player,opponent):
		index_corners=[(0,0),(7,0),(0,7),(7,7)]
		corners_player=0
		corners_opponent=0
		for (i,j) in index_corners:
			if(state.getCell(i,j)==player):
				corners_player+=1
			if(state.getCell(i,j)==opponent):
				corners_opponent+=1
		total_corners=corners_player+corners_opponent
		final_corners=0
		if(total_corners!=0):
			final_corners=100*((corners_player-corners_opponent)/total_corners)
		return final_corners
	
	#Returns dictionary with table weights
	def get_weights(self):
		return {
					(0,0):4,(0,1):-3,(0,2):2,(0,3):2,(0,4):2,(0,5):2,(0,6):-3,(0,7):4,
					(1,0):-3,(1,1):-4,(1,2):-1,(1,3):-1,(1,4):-1,(1,5):-1,(1,6):-4,(1,7):-3,
					(2,0):2,(2,1):-1,(2,2):1,(2,3):0,(2,4):0,(2,5):1,(2,6):-1,(2,7):6,
					(3,0):2,(3,1):-1,(3,2):0,(3,3):1,(3,4):1,(3,5):0,(3,6):-1,(3,7):6,
					(4,0):2,(4,1):-1,(4,2):0,(4,3):1,(4,4):1,(4,5):0,(4,6):-1,(4,7):6,
					(5,0):2,(5,1):-1,(5,2):1,(5,3):0,(5,4):0,(5,5):1,(5,6):-1,(5,7):6,
					(6,0):-3,(6,1):-4,(6,2):-1,(6,3):-1,(6,4):-1,(6,5):-1,(6,6):-4,(6,7):-3,
					(7,0):4,(7,1):-3,(7,2):2,(7,3):2,(7,4):2,(7,5):2,(7,6):-3,(7,7):4
				}
	
	#Control over the table
	def control_over_table(self,state,player,opponent,weights):
		i=0
		j=0
		control_player=0
		control_opponent=0
		for i in range(0,8):
			for j in range(0,8):
				cell=state.getCell(i,j)
				if(cell==player):
					control_player+=weights[(i,j)]
				elif(cell==opponent):
					control_opponent+=weights[(i,j)]
				else:
					continue
		total_control=abs(control_player)+abs(control_opponent)
		final_control=0
		if(total_control!=0):
			final_control=100*((control_player-control_opponent)/total_control)
		return final_control
		
	#Return the mobility of both players, watch it, we have to differenciate both cases
	def mobility(self,state,player,opponent):
		mobility=0
		if(state.player==player):
			moves_player = len(state.actions())
			state_copy = OthelloState(state)
			moves_opponent = len(state_copy.actions())
			total_moves = moves_player+moves_opponent
		elif(state.player==opponent):
			moves_opponent = len(state.actions())
			state_copy = OthelloState(state)
			moves_player = len(state_copy.actions())
			total_moves = moves_player+moves_opponent
		else:
			raise Exception
		if(total_moves!=0):
			mobility = 100*((moves_player - moves_opponent)/total_moves)
		return mobility
	
	#Return the frontier of the table
	def frontier(self,state,player,opponent):
		index_neighbors=[(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,-1),(-1,0),(-1,-1)]
		frontier_player=0
		frontier_opponent=0
		for i in range(0,8):
			for j in range(0,8):
				#Case player
				if(state.getCell(i,j)==player):
					stop=False
					z=0
					while(not stop and z<len(index_neighbors)):
						(plus_i,plus_j)=index_neighbors[z]
						try:
							if(state.getCell(i+plus_i,j+plus_j)==0):
								stop=True
								frontier_player+=1
						except Exception:
							continue
						finally:
							z+=1
				elif(state.getCell(i,j)==opponent):
					stop=False
					z=0
					while(not stop and z<len(index_neighbors)):
						(plus_i,plus_j)=index_neighbors[z]
						try:
							if(state.getCell(i+plus_i,j+plus_j)==0):
								stop=True
								frontier_opponent+=1
						except Exception:
							continue
						finally:
							z+=1
				else:
					continue
		final_frontier=0
		#We want the less frontier as possible
		total_frontier=frontier_player+frontier_opponent
		if(total_frontier!=0):
			final_frontier=100*((frontier_opponent-frontier_player)/total_frontier)
		return final_frontier
	
	#Return the stability, we measure the edge of the table from the corners, the frontier heuristic helps building around that. Also, corners are double points
	def stability(self,state,player,opponent):
		
		stability_player=0
		stability_opponent=0
		final_stability=0
		search_space=[]
		
		#Search spaces
		lower_row=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
		#lower_row_reversed=lower_row[::-1]
		left_column=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)]
		#left_column_reversed=left_column[::-1]
		right_column=[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)]
		#right_column_reversed=right_column[::-1]
		upper_row=[(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
		#upper_row_reversed=upper_row[::-1]
		search_space.extend((lower_row,left_column, right_column, upper_row))
		
		flag_search=0 #Which player are we controlling
		
		for space in search_space:
			#It is the player
			if(state.getCell(space[0][0],space[0][1])==player):
				flag_search=player
				i=0
				j=7
				#Swipe to the left
				while(flag_search==player and i<j+1):
					if(state.getCell(space[i][0],space[i][1])==player):
						stability_player+=1
						i+=1
					else:
						flag_search=opponent
				#Swipe to the right, we did not get to the end
				while(flag_search==opponent and j>i-1):
					if(state.getCell(space[j][0],space[j][1])==opponent):
						stability_opponent+=1
						j-=1
					else:
						flag_search=0
			#It is the opponent
			elif(state.getCell(space[0][0],space[0][1])==opponent):
				flag_search=opponent
				i=0
				j=7
				#Swipe to the left
				while(flag_search==opponent and i<j+1):
					if(state.getCell(space[i][0],space[i][1])==opponent):
						stability_opponent+=1
						i+=1
					else:
						flag_search=player
				#Swipe to the right, we did not get to the end
				while(flag_search==player and j>i-1):
					if(state.getCell(space[j][0],space[j][1])==player):
						stability_player+=1
						j-=1
					else:
						flag_search=0
			#No one controls this place
			else:
				continue
		
		total_stability=stability_player+stability_opponent
		if(total_stability!=0):
			final_stability=100*((stability_player-stability_opponent)/total_stability)
		return final_stability
