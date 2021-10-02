from agent_interface import AgentInterface
from random_agent import RandomAgent
from game import Game


class MarkovAgent(AgentInterface):
    """
    Markov Agent: Evaluate each action by taking it, followed by
    random plays. Action with most wins is chosen.
    """
    def __init__(self):
        self.__simulator = Game(RandomAgent(), RandomAgent())

    def info(self):
        return {"agent name": "Markov"}

    def decide(self, state, actions):
        win_counter = [0] * len(actions)
        counter = 0
        while True:
            counter += 1
            for i, action in enumerate(actions):
                state2 = state.successor(action)
                result = self.__simulator.play(output=False, starting_state=state2)
                win_counter[i] += 1 if result == state.player else 0
            yield actions[win_counter.index(max(win_counter))]
