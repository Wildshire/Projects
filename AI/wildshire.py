import random
from othello import OthelloState
from agent_interface import AgentInterface

"""
EXPLANATION:
Wildshire is an agent programmed by doing an iterative search tree. This means that until it runs out of time it will continuously create trees of bigger depth and yielding the best move at each level. Init will create two attributes for making its heuristic more dynamic as the game progresses. These are the stages of the game (it will know if it is on the early-mid-late game) and it will weigh the different heuristics according to that. The info function is to return the data and the implementation of the decide function is explained below.

The decide function works as follows:
1) Get the stage of the game
2) Update weights for the heuristics
3) Actions are sorted in the order that moves that are closer to the corners are explored first. This is quite a naive approach but sufficient to maximize the possibilities of cuts with alpha-beta while not increasing the computation cost in my opinion. Also by default, the first one is already yielded just in case times are extremely low.
3) Depth = 1
4) Create tree search starting with depth=depth+1
5) Yield the best move
6) If there is still time, go back to 4

Then the tree is constructed as the minimax function provided as the example
Let's take a look at maximizing/minimizing nodes:
1) First of all, I decided that we only count the number of coins each player when the game is finished (no actions left), as it was done originally in the minimax algorithm
2) If not, then if we are at the bottom we calculate the "score" of the board with my heuristic function
3) In the case more search is needed (need to go a deeper level), then the actions are sorted as the decided function.
4) Then we explore the sorted actions updating alpha/beta values and pruning when possible. We return the value from the bottom level.
5) And of course there is the alternation between minimizing and maximizing in each level.

The way a state is evaluated is by using my heuristic function. It calculates 5 different values and sums them up in the end by also applying the weights of the stage of the game. All heuristics calculate the value of the player and the opponent and both values are subtracted from each other.
1) Corners captured: The more corners the player has, the better.
2) Control of the table: Each position is labeled with a value, the higher this value, the more control you have on the table -> edges and corners are highly valuable plus and the center of the table as well
3) Mobility: The more moves the player has, the better.
4) Frontier: The fewer coins the player has next to a blank spot, the better.
5) Stability: The more stable coins the player has, the better (I have to say this one is not complete, it only calculates the stability on the corners and edges on the table, actually this heuristic combined with the frontier encourages the player to usually stabilize its pieces at the mid-late game)

Then each value is weighted and summed up.
"""

"""
TESTING
As for testing, I did a lot of matches against the agents provided in this exercise and Wildshire can consistently beat the minimax agents while not skipping any turn by doing a random move. Also, the alpha-beta pruning helps to explore deeper levels the more time it has (at least one level more with the same time budget). The one agent that can beat mine is the Markov agent because I know that my heuristic function is not perfect, this can happen 1 time every 10 matches on average, but I have not checked with times higher than 10 seconds.

Still, to be sure, I organized a mini tournament with my agent against Markov, minimax 2-3-4, another 3 versions of Wildshire (with different heuristics and weights), 2 versions of another agent of another classmate, and the Random agent. Each agent played against each other in a total of 40 matches with times: 5.0,7.0,10 and 15.0 and Wildshire had the best results of 33 matches won, 1 draw, and 6 losses. So the worst-case scenario is that one agent beated him 4 times but still it managed to win against the other ones.
"""


class Wildshire(AgentInterface):
	"""
	An agent who plays the Othello game
	
	Methods
	-------
	'init' prepare the weights and stages of the game
	`info` returns the agent's information
	`decide` chooses an action from possible actions
	"""
	
	def __init__(self):
		self.stages=[64,52,14]
		self.all_weights=[[100,170,200,50,50],[100,170,100,100,70],[80,100,50,150,150]]
	
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
	
		return {"agent name": "Wildshire",  # COMPLETE HERE
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
			
		#Get state of the game: early-mid-late
		empty_spaces=state.count(0) #How many spaces are
		i=0
		weights=[100,100,100,100,100] #Standard weights
		while(i<len(self.stages)):
			if(empty_spaces<self.stages[i]):
				weights=self.all_weights[i]
			i+=1
		#This is for iterative deeping
		depth=0
		while True:
			depth = depth + 1 #The depth of the tree
			alpha=float("-inf") #Try to get a high as possible
			beta=float("inf") #Try to get as low as possible
			
			#sort actions
			actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
			max_value=-10000
			choice=actions[0] #Worst case we chose this one by default
			
			#Yielding choices until we ran out of time
			for action in actions:
				new_value = self.min_value(state.successor(action), depth - 1,alpha,beta,weights)
				if(new_value>max_value):
					max_value=new_value
					choice=action
			yield choice
		
	#Maximizing node
	def max_value(self, state, depth,alpha,beta,weights):
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
					return self.min_value(OthelloState(state), depth - 1,alpha,beta,weights)
		#End of the search, my heuristic function
		if(depth==0):
			return self.heuristics(state,state.player,weights)
	
		#Sort actions
		actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
		
		#Pruning
		i=0
		stop=False
		value = float('-inf')
		while(not stop and i<len(actions)):
			value = max(value,self.min_value(state.successor(actions[i]), depth - 1,alpha,beta,weights))
			alpha = max(value, alpha)
			if alpha >= beta:
				stop=True
				continue
			i+=1	
		return value
		
	#Minimizing node	
	def min_value(self, state, depth,alpha,beta,weights):
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
					return self.max_value(OthelloState(state), depth - 1,alpha,beta,weights)
		#End of the search, my heuristic function
		if(depth==0):
			return self.heuristics(state,state.otherPlayer(),weights)
		
		#Sort actions
		actions=sorted(actions,key=lambda triple: ((triple[0]+8*triple[1])%7))
		#Pruning
		i=0
		stop=False
		value = float('inf')
		while(not stop and i<len(actions)):
			value = min(value,self.max_value(state.successor(actions[i]), depth - 1,alpha,beta,weights))
			beta = min(value,beta)
			if(beta<=alpha):
				stop=True
				continue
			i+=1	
		return value
		
	#My heuristic function
	def heuristics(self,state,player,weights):
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
		
		return weights[0]*final_corners+weights[1]*final_control+weights[2]*final_mobility+weights[3]*final_frontier+weights[4]*final_stability
	
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
			final_corners=(corners_player-corners_opponent)/total_corners
		return final_corners
	
	#Control over the table with the weights of the table
	def control_over_table(self,state,player,opponent,table):
		i=0
		j=0
		control_player=0
		control_opponent=0
		for i in range(0,8):
			for j in range(0,8):
				cell=state.getCell(i,j)
				if(cell==player):
					control_player+=table[(i,j)]
				elif(cell==opponent):
					control_opponent+=table[(i,j)]
				else:
					continue
		total_control=abs(control_player)+abs(control_opponent)
		final_control=0
		if(total_control!=0):
			final_control=(control_player-control_opponent)/total_control
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
			#This should never happen
			return mobility
		if(total_moves!=0):
			mobility = (moves_player - moves_opponent)/total_moves
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
			final_frontier=(frontier_opponent-frontier_player)/total_frontier
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
			final_stability=(stability_player-stability_opponent)/total_stability
		return final_stability

	#Extra functions
	#Returns dictionary with table weights for table control
	def get_weights(self):
		return {
					(0,0):4,(0,1):-3,(0,2):2,(0,3):2,(0,4):2,(0,5):2,(0,6):-3,(0,7):4,
					(1,0):-3,(1,1):-4,(1,2):-1,(1,3):-1,(1,4):-1,(1,5):-1,(1,6):-4,(1,7):-3,
					(2,0):2,(2,1):-1,(2,2):1,(2,3):0,(2,4):0,(2,5):1,(2,6):-1,(2,7):2,
					(3,0):2,(3,1):-1,(3,2):0,(3,3):1,(3,4):1,(3,5):0,(3,6):-1,(3,7):2,
					(4,0):2,(4,1):-1,(4,2):0,(4,3):1,(4,4):1,(4,5):0,(4,6):-1,(4,7):2,
					(5,0):2,(5,1):-1,(5,2):1,(5,3):0,(5,4):0,(5,5):1,(5,6):-1,(5,7):2,
					(6,0):-3,(6,1):-4,(6,2):-1,(6,3):-1,(6,4):-1,(6,5):-1,(6,6):-4,(6,7):-3,
					(7,0):4,(7,1):-3,(7,2):2,(7,3):2,(7,4):2,(7,5):2,(7,6):-3,(7,7):4
				}
	
	
