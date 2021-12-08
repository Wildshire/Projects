import numpy as np
"""
This file contains the definition of the environment
in which the agents are run.
"""

import gym, gym_bandits


class AbstractEnvironment:
    def __init__(self):
        """Instanciate a new environement in its initial state.
        """
        self.env = gym.make("BanditTenArmedRandomRandom-v0")
        # self.env.env.p_dist = np.random.uniform(size=10)
        # self.env.env.r_dist = np.full(10, 1)
        self.env.seed(np.random.randint(100000000))
        self.env.reset()
        self.possible_actions = list(range(self.env.env.n_bandits))

    def act(self, action):
        """Perform given action by the agent on the environment,
        and returns a reward.
        """
        _, r, _, _ = self.env.step(action)
        return r

    def get_optimal_arm(self):
        return np.argmax(self.env.env.p_dist)

class Env1(AbstractEnvironment):
  def __init__(self):
    AbstractEnvironment.__init__(self)
    self.env = gym.make("BanditTwoArmedHighLowFixed-v0")
    self.env.seed(np.random.randint(100000000))
    self.env.reset()
    self.possible_actions = list(range(self.env.env.n_bandits))

class Env2(AbstractEnvironment):
  def __init__(self):
    AbstractEnvironment.__init__(self)
    self.env = gym.make("BanditTwoArmedHighHighFixed-v0")
    self.env.seed(np.random.randint(100000000))
    self.env.reset()
    self.possible_actions = list(range(self.env.env.n_bandits))

class Env3(AbstractEnvironment):
  def __init__(self):
    AbstractEnvironment.__init__(self)
    self.env = gym.make("BanditTwoArmedLowLowFixed-v0")
    self.env.seed(np.random.randint(100000000))
    self.env.reset()
    self.possible_actions = list(range(self.env.env.n_bandits))

class Env4(AbstractEnvironment):
  def __init__(self):
    AbstractEnvironment.__init__(self)
