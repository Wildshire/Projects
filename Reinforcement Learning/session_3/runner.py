"""
This is the machinnery that runs your agent in an environment.

This is not intented to be modified during the practical.
"""
import numpy as np
import agents


def iter_or_loopcall(o, count, **kwargs):
    if callable(o):
        return [ o(**kwargs) for _ in range(count) ]
    else:
        # must be iterable
        return list(iter(o))

class OptimalBandit:
    def __init__(self, optimal):
        """Init.
        """
        self.optimal = optimal

    def choose(self):
        """Acts in the environment.

        returns the chosen action.
        """
        return self.optimal

    def update(self, action, reward):
        pass

class BatchRunner:
    """
    Runs several instances of the same RL problem in parallel
    and aggregates the results.
    """

    def __init__(self, env_maker, agent_maker, count, verbose=False):
        self.environments = iter_or_loopcall(env_maker, count)
        if agent_maker == "OptimalArm":
            self.agents = [OptimalBandit(optimal=_.get_optimal_arm()) for _ in self.environments]
        else:
            self.agents = iter_or_loopcall(eval('agents.{}'.format(agent_maker)), count, arms=self.environments[0].possible_actions)
        assert(len(self.agents) == len(self.environments))
        self.verbose = verbose

    def step(self):
        actions = [ agent.choose() for (agent) in self.agents ]
        rewards = [ env.act(action) for (env, action) in zip(self.environments, actions)]
        optimal_actions = [int(_.get_optimal_arm()!=a) for _, a in zip(self.environments, actions)]
        for (agent, action, reward) in zip(self.agents, actions, rewards):
            agent.update(action, reward)
        return rewards, optimal_actions

    def loop(self, iterations):
        list_reward = []
        list_nb_suboptimal = []
        for i in range(1, iterations+1):
            rewards, optimal_actions = self.step()
            list_reward.append(rewards)
            list_nb_suboptimal.append(optimal_actions)
            if self.verbose:
                print("Simulation step {}:".format(i))
                print(" ->            average reward: {}".format(np.mean(list_reward)))
                # print(" -> cumulative average reward: {}".format(cum_avg_reward))
        list_reward = np.cumsum(np.array(list_reward), 0)
        list_nb_suboptimal = np.cumsum(np.array(list_nb_suboptimal), 0)
        return list_reward, list_nb_suboptimal
