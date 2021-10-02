import random
from othello import OthelloState
from agent_interface import AgentInterface


class Agent(AgentInterface):
    """
    This agent is an implementation of Alpha-Beta searching algorithm, with the additional of
    advance heuristic value function.

    The heuristic value function is the combination of following elements:
    1. Coin count: The difference in number of coins between max player and min player
    2. Mobility: The ability to have available actions between max player and min player
    3. Corners and edges: Corners and edges have higher weight, since it's better to capture these place
    4. Stability: The measurement indicates the possibility of being changed into different color.

    This agent beats Markov Agent with THE WINNING RATE OF 66% in 12 testing games.

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

        return {"agent name": "Dylan\'s Agent",  # COMPLETE HERE
                "student name": ["Dylan N Pham"],  # COMPLETE HERE
                "student number": ["899376"]}  # COMPLETE HERE

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
        values = {}
        alpha = - float('inf')
        beta = float('inf')
        depth = 4
        for action in actions:
            values[action] = self.min_value(state.successor(action), depth - 1, alpha, beta)
        max_value = max(values.values())
        candidates = [action for action in actions if (values[action] - max_value > -1)]
        yield random.choice(candidates)


    def max_value(self, state, depth, alpha, beta):
        actions = state.actions()
        if not actions:
            if (not state.previousMoved):
                if (state.count(state.player)>state.count(state.otherPlayer)):
                    return 10000
                if (state.count(state.player)<state.count(state.otherPlayer)):
                    return -10000
                return self.stateValue(state, state.player)
            else:
                if not (depth == 0):
                    return self.min_value(OthelloState(state), depth - 1, alpha, beta)
        if depth == 0:
            return self.stateValue(state, state.player)
        value = float('-inf')
        for action in actions:
            value = max(value, self.min_value(state.successor(action), depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value


    def min_value(self, state, depth, alpha, beta):
        actions = state.actions()
        if not actions:
            if (not state.previousMoved):
                if (state.count(state.player) < state.count(state.otherPlayer)):
                    return 10000
                if (state.count(state.player) > state.count(state.otherPlayer)):
                    return -10000
                return self.stateValue(state, state.otherPlayer())
            else:
                if not (depth == 0):
                    return self.max_value(OthelloState(state), depth - 1, alpha, beta)
        if depth == 0:
            return self.stateValue(state, state.otherPlayer())
        value = float('inf')
        for action in actions:
            value = min(value, self.max_value(state.successor(action), depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value



    def stateValue(self, state:OthelloState, player):
        # define current player
        me = player
        op = 3 - player

        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

        V = [[20, -3, 11, 8, 8, 11, -3, 20],
             [-3, -7, -4, 1, 1, -4, -7, -3],
             [11, -4, 2, 2, 2, 2, -4, 11],
             [8, 1, 2, -3, -3, 2, 1, 8],
             [8, 1, 2, -3, -3, 2, 1, 8],
             [11, -4, 2, 2, 2, 2, -4, 11],
             [-3, -7, -4, 1, 1, -4, -7, -3],
             [20, -3, 11, 8, 8, 11, -3, 20]]


        # Piece difference, frontier disks and disk squares
        d = 0
        my_tiles = 0
        opp_tiles = 0
        my_front_tiles = 0
        opp_front_tiles = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if state.getCell(i, j) == me:
                    d += V[i][j]
                    my_tiles = my_tiles + 1
                elif state.getCell(i, j) == op:
                    d -= V[i][j]
                    opp_tiles = opp_tiles + 1
                if not state.getCell(i, j) == 0:
                    for k in range(0, 8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if (x >= 0 and y >= 0) and (x < 8 and y < 8):
                            if state.getCell(x, y) == 0:
                                if state.getCell(i, j) == me:
                                    my_front_tiles = my_front_tiles + 1
                                else:
                                    opp_front_tiles = opp_front_tiles + 1
                                break

        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0

        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0


        # Corner occupancy
        my_tiles = 0
        opp_tiles = 0
        if state.getCell(0, 0) == me: my_tiles = my_tiles + 1
        elif state.getCell(0, 0) == op: opp_tiles = opp_tiles + 1

        if state.getCell(0, 7) == me: my_tiles = my_tiles + 1
        elif state.getCell(0, 7) == op: opp_tiles = opp_tiles + 1

        if state.getCell(7, 0) == me: my_tiles = my_tiles + 1
        elif state.getCell(7, 0) == op: opp_tiles = opp_tiles + 1

        if state.getCell(7, 7) == me: my_tiles = my_tiles + 1
        elif state.getCell(7, 7) == op: opp_tiles = opp_tiles + 1
        c = 25 * (my_tiles - opp_tiles)

        # Corner closeness
        my_tiles = 0
        opp_tiles = 0
        if state.getCell(0, 0) == 0:
            if state.getCell(0, 1) == me: my_tiles = my_tiles + 1
            elif state.getCell(0, 1) == op: opp_tiles = opp_tiles + 1
            if state.getCell(1, 1) == me: my_tiles = my_tiles + 1
            elif state.getCell(1, 1) == op: opp_tiles = opp_tiles + 1
            if state.getCell(1, 0) == me: my_tiles = my_tiles + 1
            elif state.getCell(1, 0) == op: opp_tiles = opp_tiles + 1

        if state.getCell(0, 7) == 0:
            if state.getCell(0, 6) == me: my_tiles = my_tiles + 1
            elif state.getCell(0, 6) == op: opp_tiles = opp_tiles + 1
            if state.getCell(1, 6) == me: my_tiles = my_tiles + 1
            elif state.getCell(1, 6) == op: opp_tiles = opp_tiles + 1
            if state.getCell(1, 7) == me: my_tiles = my_tiles + 1
            elif state.getCell(1, 7) == op: opp_tiles = opp_tiles + 1

        if state.getCell(7, 0) == 0:
            if state.getCell(7, 1) == me: my_tiles = my_tiles + 1
            elif state.getCell(7, 1) == op: opp_tiles = opp_tiles + 1
            if state.getCell(6, 1) == me: my_tiles = my_tiles + 1
            elif state.getCell(6, 1) == op: opp_tiles = opp_tiles + 1
            if state.getCell(6, 0) == me: my_tiles = my_tiles + 1
            elif state.getCell(6, 0) == op: opp_tiles = opp_tiles + 1

        if state.getCell(7, 7) == 0:
            if state.getCell(6, 7) == me: my_tiles = my_tiles + 1
            elif state.getCell(6, 7) == op: opp_tiles = opp_tiles + 1
            if state.getCell(6, 6) == me: my_tiles = my_tiles + 1
            elif state.getCell(6, 6) == op: opp_tiles = opp_tiles + 1
            if state.getCell(7, 6) == me: my_tiles = my_tiles + 1
            elif state.getCell(7, 6) == op: opp_tiles = opp_tiles + 1
        l = -12.5 * (my_tiles - opp_tiles)

        # Mobility
        my_tiles = 0
        opp_tiles = 0
        actions = state.actions()
        for _, _, player in actions:
            if player == me:
                my_tiles = my_tiles + 1
            else:
                opp_tiles = opp_tiles + 1
        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0

        # final function
        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (10 * d) + (74.396 * f)
        return score