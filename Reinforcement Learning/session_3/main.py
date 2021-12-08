import argparse
import environment
import runner
import random
import time
from matplotlib import pyplot as plt
from matplotlib.gridspec import SubplotSpec

parser = argparse.ArgumentParser(description='RL running machine')
list_bandits_algs = ['UniformBandit', 'OptimalArm', 'epsGreedyBandit', 'UCB1Bandit', 'BesaBandit', 'ThompsonBandit', 'KLUCBBandit']
list_colors = ["yellow", "black", "red", "green", "blue", "purple", "darkorange"]
parser.add_argument('--agents', nargs="+",
                        choices=list_bandits_algs,
                        default=list_bandits_algs)
parser.add_argument('--niter', type=int, metavar='n', default=10000, help='number of iterations to simulate')
parser.add_argument('--nruns', type=int, metavar='nagent', help='Number of parallel runs', default=5)
parser.add_argument('--verbose', action='store_true', help='Display cumulative results at each step')

random.seed(0)

def plot_bandit(ax, rewards, label, color):
    cum_rewards, error_bar = rewards.mean(1), rewards.std(1)
    t = list(range(len(cum_rewards)))
    ax.plot(t, cum_rewards, label=label, color=color)
    ax.fill_between(t, cum_rewards+error_bar, cum_rewards-error_bar, facecolor=color, alpha=0.1)
    ax.set_xlabel("Iter")
    ax.set_ylabel("Cum. Reward")

def plot_suboptimal_action(ax, nb_suboptimal, label, color):
    cum_nb_suboptimal, error_bar = nb_suboptimal.mean(1), nb_suboptimal.std(1)
    t = list(range(len(cum_nb_suboptimal)))
    ax.plot(t, cum_nb_suboptimal, label=label, color=color)
    ax.fill_between(t, cum_nb_suboptimal+error_bar, cum_nb_suboptimal-error_bar, facecolor=color, alpha=0.1)
    ax.set_xlabel("Iter")
    ax.set_ylabel("Nb suboptimal draws")


def create_subtitle(fig: plt.Figure, grid: SubplotSpec, title: str):
    "Sign sets of subplots with title"
    row = fig.add_subplot(grid)
    # the '\n' is important
    row.set_title(f'{title}\n', fontweight='semibold')
    # hide subplot
    row.set_frame_on(False)
    row.axis('off')


def main():
    args = parser.parse_args()



    print("--> Setup: {} iterations for {} (independent) simulations.".format(args.niter, args.nruns))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 2, figsize=(6,12))
    grid = plt.GridSpec(4, 2)
    idx = 0

    for ax, env_class_name in [(ax1, "Env1"), (ax2, "Env2"), (ax3, "Env3"), (ax4, "Env4")]:
        print("#" * 15)
        env_class = eval('environment.{}'.format(env_class_name))


        for id_agent, agent_class in enumerate(args.agents):
            try:
                start_t = time.time()
                runner_optimal = runner.BatchRunner(env_class, agent_class, args.nruns, args.verbose)
                list_cumul, nb_suboptimal_act = runner_optimal.loop(args.niter)
                print("Runtime of {} on {}: {}".format(agent_class, env_class_name, time.time() - start_t))

                plot_bandit(ax[0], list_cumul, agent_class, list_colors[id_agent])
                plot_suboptimal_action(ax[1], nb_suboptimal_act, agent_class, list_colors[id_agent])
            except NotImplementedError:
                print("<Agent {} is not implemented.>".format(agent_class))

        env = env_class()
        ax[1].set_xscale("log")
        ax[1].set_ylim((0,500))
        ax[1].set_xlim((100,args.niter))
        create_subtitle(fig, grid[idx, ::], "[{}] Nb bandits: {}; Reward dist: {}".format(env_class_name, env.env.n_bandits, ["{:.2f}".format(_) for _ in env.env.p_dist]))
        idx += 1

    lines_labels = [ax1[0].get_legend_handles_labels()]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines, labels, loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)

    plt.show()

if __name__ == "__main__":
    main()
