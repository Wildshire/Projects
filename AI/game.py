from agent_interface import AgentInterface
from othello import OthelloState
from copy import deepcopy
from time_limit import time_limit
from random import choice


class Game:
	def __init__(self, player1: AgentInterface, player2: AgentInterface):
		self.__players = [None, player1, player2]
	
	def play(self, output=False, starting_state=OthelloState(), timeout_per_turn=None):
		players = ['.', 'O', 'X']
		state, winner = self.__play(output, deepcopy(starting_state), timeout_per_turn)
		if output:
			print("Game ends.")
			for p in [1, 2]:
				print(f"{players[p]}) {self.__players[p].info()['agent name']}: {state.count(p)}")
			if winner == 0:
				print("The game ended in a draw!")
			else:
				print(f"Player {winner} ({players[winner]}), {self.__players[winner].info()['agent name']}, WON!")
		if winner==0:
			return None,None
		else:
			return self.__players[winner],self.__players[3-winner]
	
	def __play(self, output, state, timeout_per_turn):
		while True:
			actions = state.actions()
			if len(actions) == 0 and not state.previousMoved:
				return state, (state.count(1) != state.count(2)) + (state.count(2) > state.count(1))
			if len(actions) > 0:
				action = self.__get_action(self.__players[state.player], state, actions, timeout_per_turn)
				action = choice(actions) if action is None else action
				state = state.successor(action)
			else:
				state = OthelloState(state)
			if output:
				state.printstate()
				print("")
	
	def __get_action(self, player, state, actions, timeout):
		action = None
		try:
			with time_limit(timeout):
				for decision in player.decide(state, actions):
					action = decision
		except TimeoutError:
			if action is None:
				print(f"Timeout for player: {self.__players[state.player].info()['agent name']}")
		return action
	
