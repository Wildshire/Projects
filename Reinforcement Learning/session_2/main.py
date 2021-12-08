import argparse
import agents
import environment
import runner
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='test bed for dynamic programming algorithms')

subparsers = parser.add_subparsers(dest='agent')
subparsers.required = True

parser_RD = subparsers.add_parser(
    'RD', description='Random Agent')
parser_VI = subparsers.add_parser(
    'VI', description='Value Iteration agent')
parser_PI = subparsers.add_parser(
    'PI', description='Policy Iteration agent')
parser_QL = subparsers.add_parser(
    'QL', description='Q-Learning agent')

parsers = [parser_RD, parser_VI, parser_PI, parser_QL]

arg_dico = {'RD': agents.Agent,
            'VI': agents.ValueIteration,
            'PI': agents.PolicyIteration,
            'QL': agents.QLearning
            }

def plot_q_learning(sum_of_rewards, list_legends, name, policy):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    for sum_rew, legend in zip(sum_of_rewards, list_legends):
        ax1.plot(sum_rew, label=legend)
    ax1.set_xlabel('Episodes')
    ax1.set_ylabel('Sum of rewards')

    action = {0: "U", 1: "R", 2: "D", 3: "L"}
    optimal_policy = []

    grid = np.ones((4, 12))
    grid[3, 1:-1] = 0
    policy = policy.reshape((4, 4, 12))
    # extent = (0, 11, 3, 0)
    ax2.imshow(grid)
    ax2.set_xticks(np.arange(0, 12, 1))
    ax2.set_yticks(np.arange(0, 4, 1))
    ax2.set_xticklabels(np.arange(0, 12, 1))
    ax2.set_yticklabels(np.arange(0, 4, 1))
    ax2.grid(color='w', linewidth=2)
    ax2.set_frame_on(False)


    for i in range(4):
        for j in range(12):
            if i != 3:
                ax2.text(j, i, '{}'.format("\n".join(["{}: {:0.2f}".format(action[idaction], _) for idaction, _ in enumerate(policy[:, i, j])])), size=6, ha='center', va='center')
            else:
                if j == 0:
                    ax2.text(j, i, '{}'.format("\n".join(["{}: {:0.2f}".format(action[idaction], _) for idaction, _ in enumerate(policy[:, i, j])])), size=6, ha='center', va='center')
                elif j == 11:
                    ax2.text(j, i, 'GOAL', ha='center', va='center')
                else:
                    ax2.text(j, i, '-', ha='center', va='center')
    ax2.set_title("Q values")

    fig.tight_layout()
    plt.show()

def plot_policy(policy, V, name):
    # Action in [UP, RIGHT, DOWN, LEFT]
    action = {0: "Up", 1: "Right", 2: "Down", 3: "Left"}
    optimal_policy = []

    for id_r, row in enumerate(policy.argmax(1).reshape((4, 12))):
        row_l = []
        for id_c, col in enumerate(row):
            if id_r != 3:
                row_l.append(action[col])
            else:
                if id_c == 0:
                    row_l.append(action[col])
                elif id_c == 11:
                    row_l.append("Goal")
                else:
                    row_l.append("-")
        optimal_policy.append(row_l)
    return optimal_policy



def run_agent(nb_episodes, args):
    env_class = environment.Environment()
    agent_class = arg_dico[args.agent]

    # print("Running a single instance simulation...")
    name = args.agent
    my_runner = runner.Runner(env_class, agent_class(env_class), name)
    if name in ["RD", "QL"]:
        final_reward, policy = my_runner.loop(nb_episodes)
        plot_q_learning([final_reward], [args.agent], name, policy)
    elif name in ["PI", "VI"]:
        policy, V = my_runner.loop(nb_episodes)
        decsions = plot_policy(policy, V, name)
        plt.matshow(V.reshape((4, 12)))
        action = {0: "U", 1: "R", 2: "D", 3: "L"}
        for (i, j), z in np.ndenumerate(V.reshape((4, 12))):
            plt.text(j, i, '{:0.1f} [{}]'.format(z, decsions[i][j]), ha='center', va='center')
        plt.title("Policy iteration" if name == "PI" else "Value iteration")
        plt.show()

def main():
    nb_episodes = 500
    args = parser.parse_args()
    if args.agent != "ALL":
        run_agent(nb_episodes, args)

if __name__ == "__main__":
    main()
