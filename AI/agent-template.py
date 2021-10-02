from othello import OthelloState
from agent_interface import AgentInterface


class Agent(AgentInterface):
    """
    An agent who plays the Othello game

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """

    @staticmethod
    def info():
        """
        Return the agent's information

        Returns
        -------
        Dict[str, str]
            `agent name` is the agent's name
            `student name` is the list team members' names
            `student number` is the list of student numbers of the team members
        """
        # -------- Task 1 -------------------------
        # Please complete the following information

        return {"agent name": "?",  # COMPLETE HERE
                "student name": ["?"],  # COMPLETE HERE
                "student number": ["?"]}  # COMPLETE HERE

    def decide(self, state: OthelloState, actions: list):
        """
        Generate a sequence of increasingly preferable actions

        Given the current `state` and all possible `actions`, this function
        should choose the action that leads to the agent's
        victory.
        However, since there is a time limit for the execution of this function,
        it is possible to choose a sequence of increasing preferable actions.
        Therefore, this function is designed as a generator; it means it should
        have no return statement, but it should `yield` a sequence of increasing
        good actions.

        IMPORTANT: If no action is yielded within the time limit, the game will
        choose a random action for the player.

        Parameters
        ----------
        state: OthelloState
            Current state of the board
        actions: list
            List of all possible actions

        Yields
        ------
        action
            the chosen `action`
        """
        # -------- TASK 2 ------------------------------------------------------
        # Your task is to implement an algorithm to choose an action form the
        # given `actions` list. You can implement any algorithm you want.
        # However, you should keep in mind that the execution time of this
        # function is limited. So, instead of choosing just one action, you can
        # generate a sequence of increasing good action.
        # This function is a generator. So, you should use `yield` statement
        # rather than `return` statement. To find more information about
        # generator functions, you can take a look at:
        # https://www.geeksforgeeks.org/generators-in-python/
        #
        # If you generate multiple actions, the last action will be used in the
        # game.
        #
        # Tips
        # ====
        # 1. During development of your algorithm, you may want to find the next
        #    state after applying an action to the current state; in this case,
        #    you can use the following patterns:
        #    `next_state = current_state.successor(action)`
        #
        # 2. If you need to simulate a game from a specific state to find the
        #    the winner, you can use the following pattern:
        #    ```
        #    simulator = Game(FirstAgent(), SecondAgent())
        #    winner = simulator.play(starting_state=specified_state)
        #    ```
        #    The `MarkovAgent` has illustrated a concrete example of this
        #    pattern.
        #
        # 3. You are free to choose what kind of game-playing agent you
        #    implement. Some of the obvious approaches are the following:
        # 3.1 Implement alpha-beta (and investigate its potential for searching deeper
        #     than what is possible with Minimax). Also, the order in which the actions
        #     are tried in a given node impacts the effectiveness of alpha-beta: you could
        #     investigate different ways of ordering the actions/successor states.
        # 3.2 Try out better heuristics, e.g. ones that take into account the higher
        #     importance of edge and corner cells. Find material on this in the Internet.
        # 3.3 You could try out more advanced Monte Carlo search methods (however, we do
        #     not know whether MCTS is competitive because of the high cost of the full
        #     gameplays.)
        # 3.4 You could of course try something completely different if you are willing to
        #     invest more time.
        #
        # GL HF :)
        # ----------------------------------------------------------------------

        # Replace the following lines with your algorithm
        best_action = actions[0]
        yield best_action
