"""
This is the machinnery that runs your agent in an environment.

This is not intented to be modified during the practical.
"""
import subprocess as sp


class Runner:
    def __init__(self, environment, agent, name):
        self.environment = environment
        self.agent = agent
        self.name = name

    def step(self):
        observation = self.environment.observe()
        action = self.agent.action(observation)
        reward, done = self.environment.act(action)
        self.agent.update(observation, action, reward)
        return (observation, action, reward, done)

    def loop(self, n_episodes):
        if self.name in ["RD", "QL"]:
            list_sum_reward = []

            for i in range(1, n_episodes + 1):
                cumul_reward = 0.0
                done = False

                while not done:
                    (obs, act, rew, done) = self.step()
                    cumul_reward += rew
                print("Episode ", i, " cumul reward ", cumul_reward)
                self.environment.env.reset()
                list_sum_reward.append(cumul_reward)

            return list_sum_reward, self.agent.policy
        elif self.name == "PI":
            return self.agent.policy_iteration()
        else:
            return self.agent.value_iteration()
