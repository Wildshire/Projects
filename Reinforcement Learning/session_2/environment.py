"""
This file contains the definition of the environment
in which the agents are run.
Do not modify this file
"""
from gym.envs.toy_text import cliffwalking
import numpy as np
import sys
from gym.envs.toy_text import discrete

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Environment:
    # List of the possible actions by the agents
    possible_actions = [0, 1, 2, 3] # UP, RIGHT, DOWN, LEFT
    final_states = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]

    def __init__(self):
        """Instanciate a new environement in its initial state.
        """
        self.env = cliffwalking.CliffWalkingEnv()

    def observe(self):
        """Returns the current observation that the agent can make
        of the environment, if applicable.
        """
        return self.env.s

    def act(self, action):
        """Perform given action by the agent on the environment,
        and returns a reward.
        """
        observation, reward, done, _ = self.env.step(action)
        if not done:
            return reward, done
        else:
            return 0, done

    def get_reward(self, state):
        if state in [37, 38, 39, 40, 41, 42, 43, 44, 45, 46]:
            return -100
        else:
            return -1
