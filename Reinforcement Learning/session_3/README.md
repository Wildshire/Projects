


# Bandit algorithms, Practical session 3
In this third practical, you are asked to put what you just learnt
about bandits to good use. You are provided with the `main.py` file,
a bandits test bed. Use `python main.py -h` to check how you are
supposed to use this file.

![image not found:](multiarmedbandit.jpg "Bandits")

Install:
``pip install --user git+https://github.com/mimoralea/gym-bandits#egg=gym-bandits``

You will implement:
* Epsilon-greedy bandit
* UCB1 https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf
* Thompson sampling Bandit https://web.stanford.edu/~bvr/pubs/TS_Tutorial.pdf (chapter 3)
* Besa https://hal.archives-ouvertes.fr/hal-01025651v1/document
* KL-UCB https://arxiv.org/pdf/1102.2490.pdf


Each agent will be tested on 4 different environments:
* Env1: two-armed bandit (high difference): A_1 ~ Bernoulli(0.8) and A_2 ~ Bernoulli(0.2)
* Env2: two-armed bandit (both high rewards): A_1 ~ Bernoulli(0.8) and A_2 ~ Bernoulli(0.9)
* Env3: two-armed bandit (both low rewards): A_1 ~ Bernoulli(0.1) and A_2 ~ Bernoulli(0.2)
* Env4: ten-armed bandit: A_i ~ Bernoulli(p_i) with p_i ~ Uniform(0, 1) for i < 10.


## How do I proceed ?
Implement the 5 algorithms (mentioned above) to the ``agents.py`` file. Remove the exception raising part, and complete the two blank methods for each Bandit class.

In `__init__`, build the buffers your agent requires.
It might be interesting, for instance, to store the
number of time each action has been selected.

In `choose`, prescribe how the agent selects its
actions (the method must return an arm, that is
an index).

Finally, in `update`, implement how the agent updates
its buffers, using the newly observed `arm` and `reward`.


## Grading ?

The assessment will be based on:
* Implementation of the 5 agents (epsGreedyBandit, UCB1Bandit, BesaBandit, ThompsonBandit, KLUCBBandit) in the `agents.py` file.
* Efficiency and scalability of the code (check with: `python3 main.py --nruns 10 --niter 20000`).

Send `agents.py` to heri(at)lri(dot)fr before December, 8th 2021 at 23:59.
