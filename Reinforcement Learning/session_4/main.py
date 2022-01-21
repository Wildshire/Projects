import argparse
import agents
import environment
import runner
import sys
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Practical Session on Function Approximation')
parser.add_argument('--agent', metavar='AGENT_CLASS', choices=['MC-VL', 'TD0-VL', 'TDLambda-VL', 'TD0-QL', 'DPS'], default='TDLambda-VL', type=str, help='Class to use for the agent. Must be in the \'agents\' module. Possible choice: (MC-VL, TD0-VL, TDLambda-VL, TD0-QL, DPS)')
parser.add_argument('--nepisodes', type=int, metavar='n', default='100', help='number of episodes to simulate')
parser.add_argument('--verbose', action='store_true', help='Display cumulative results at each step')

def main():
    args = parser.parse_args()
    print("Run Function Approximation Experiment:", args)
    if args.agent == "TD0-QL":
        agent_class = agents.TD0_Q_Learning_Function_Approximation
        type_value = "state_action_value"
    elif args.agent == "MC-VL":
        agent_class = agents.MC_State_Value_Approximation
        type_value = "state_value"
    elif args.agent == "TD0-VL":
        agent_class = agents.TD0_State_Value_Approximation
        type_value = "state_value"
    elif args.agent == "TDLambda-VL":
        agent_class = agents.TDLambda_State_Value_Approximation
        type_value = "state_value"


    if args.agent != "DPS":
        env_class = environment.Mountain
        my_runner = runner.FARunner(env_class(), agent_class(), type_value, args.verbose)
        final_reward, list_n_episodes = my_runner.loop(args.nepisodes, 0)
    else:
        import gym
        print("Training ...")
        agent = agents.Direct_Policy_Search_Agent()
        print("Evaluate learned policy")
        env = gym.make("MountainCar-v0")
        for _ in range(10):
            done = False
            observation = env.reset()
            while not done:
                env.render()
                observation, reward, done, info = env.step(agent.act(observation)) # take a random action
        env.close()


if __name__ == "__main__":
    main()
