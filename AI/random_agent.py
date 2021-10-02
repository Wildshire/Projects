import random
from agent_interface import AgentInterface


class RandomAgent(AgentInterface):
    @staticmethod
    def info():
        return {"agent name": "Random"}

    def decide(self, state, actions):
        yield random.choice(actions)
