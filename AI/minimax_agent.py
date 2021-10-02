import random
from agent_interface import AgentInterface
from othello import OthelloState

class MinimaxAgent(AgentInterface):
    """
    An agent who plays the Othello game using Minimax algorithm
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """

    def __init__(self, depth):
        """
        `depth` is the limit on the depth of Minimax tree
        """
        self.depth = depth

    def info(self):
        return {"agent name": f"Minimax({self.depth})"}

    def decide(self, state, actions):
        """
        Get the value of each action by passing its successor to min_value
        function. Randomly choose from the actions with the maximum value.
        
        NOTE: `(values[action] - max_value > -1)` enforces choosing randomly
        from the actions with the exact maximum value. By replacing `-1` with
        `-k`, candidates with lower values can be considered too.
        
        """
        values = {}
        for action in actions:
            values[action] = self.min_value(state.successor(action), self.depth - 1)
        max_value = max(values.values())
        candidates = [action for action in actions if (values[action] - max_value > -1)]
        yield random.choice(candidates)

    def max_value(self, state, depth):
        """
        Get the value of each action by passing its successor to min_value
        function. Return the maximum value of successors.
        
        `max_value` sees the game from players's perspective.
        
        NOTE: when passing the successor to min_value, `depth` must be
        reduced by 1, as we go down the Minimax tree. If `depth` is equal to
        zero or the game is finished (i.e., there are no applicable actions)
        then the number of root player's pieces is returned as the value.
        
        IMPORTANT NOTE: the player must check if it is the winner (or loser)
        of the game, in which case, a large value (or a negative value) must
        be assigned to the state. This is done by  checking if the previous turn
        has been a move or a pass. In case it has been a pass, i.e. 
        `(not state.previousMoved)`, an empty list of actions means the game
        must end. If the game continues, the depth must also be checked.
        
        """
        actions = state.actions()
        if not actions:
            if (not state.previousMoved):
                if (state.count(state.player)>state.count(state.otherPlayer)):
                    return 10000
                if (state.count(state.player)<state.count(state.otherPlayer)):
                    return -10000
                return state.count(state.player)
            else:
                if not (depth == 0):
                    return self.min_value(OthelloState(state), depth - 1)
        if depth == 0:
            return state.count(state.player)
        value = float('-inf')
        for action in actions:
            value = max(value, self.min_value(state.successor(action), depth - 1))
        return value

    def min_value(self, state, depth):
        """
        Get the value of each action by passing its successor to max_value
        function. Return the minimum value of successors.
        
        `min_value` sees the game from opponent's perspective, trying to
        minimize the value of next state.
        
        NOTE: when passing the successor to max_value, `depth` must be
        reduced by 1, as we go down the Minimax tree. If `depth` is equal to
        zero or the game is finished (i.e., there are no applicable actions)
        then the number of root players's pieces (i.e., 3 - state.player) is
        returned as the value.

        IMPORTANT NOTE: the opponent must check if it is the winner (or loser)
        of the game, in which case, a negative value (or a large value) must
        be assigned to the state. This is done by checking if the previous turn
        has been a move or a pass. In case it has been a pass, i.e. 
        `(not state.previousMoved)`, an empty list of actions means the game
        must end. If the game continues, the depth must also be checked.
        """
        actions = state.actions()
        if not actions:
            if (not state.previousMoved):
                if (state.count(state.player)<state.count(state.otherPlayer)):
                    return 10000
                if (state.count(state.player)>state.count(state.otherPlayer)):
                    return -10000
                return state.count(3 -state.player)
            else:
                if not (depth == 0):
                    return self.max_value(OthelloState(state), depth - 1)
        if depth == 0:
            return state.count(3 - state.player)
        value = float('inf')
        for action in actions:
            value = min(value, self.max_value(state.successor(action), depth - 1))
        return value