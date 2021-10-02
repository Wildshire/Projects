import random
from agent_interface import AgentInterface
from othello import OthelloState

# The agent uses alpha-beta pruning search with iterative deepening
# It employs a custom heuristics:
# 1. weighting for specific squares
# 2. dynamically changing weights in corner region when corner is occupied
# 3. an additional corner occupying heuristic 
# 4. mobility heuristic
# 5. potential mobility heuristic
# 6. coin parity heurstic
# 7. coin flip heuristic
# each heuristic is weighted. The idea was to learn good values for those weights by playing 
# test games agains different agents. 
# The weighst change dynamically during game play with 

square_weights = [
            150, -20,  20,   5,   5,  20, -20, 150,
            -20, -50,  -5,  -5,  -5,  -5, -50, -20,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            -20, -50,  -5,  -5,  -5,  -5, -50, -20,
            150, -20,  20,   5,   5,  20, -20, 150 ]
corners = dict()
corners[0] = [(1,40),(8,40),(9,5)]
corners[7] = [(6,40),(15,40),(14,5)]
corners[56] = [(48,40),(57,40),(49,5)]
corners[63] = [(55,40),(56,40),(54,5)]
neighbour_squares= [-9,-8,-7,-1,+1,+7,+8,+9]

visited_states = dict()


class ABHTABAgent(AgentInterface):
    """
    An agent who plays the Othello game using Minimax algorithm
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """

    def __init__(self):
        """
        `depth` is the limit on the depth of Minimax tree
        """
        self.weights = [120,1.7,30,20] # weights
        # print (self.weights)

    def info(self):
        return {"agent name": "ABHTABAgent AKA THE SUPER RESHUFFLER",  # COMPLETE HERE
        "student name": ["Oliver Kalleinen"],  # COMPLETE HERE
        "student number": ["007"]}  # COMPLETE HERE

    def decide(self, state, actions):
        """
        Get the value of each action by passing its successor to min_value
        function. Randomly choose from the actions with the maximum value.
        
        NOTE: `(values[action] - max_value > -1)` enforces choosing randomly
        from the actions with the exact maximum value. By replacing `-1` with
        `-k`, candidates with lower values can be considered too.
        
        """
        global prunecount 
        prunecount = 0
        depth = 0
        sorted_actions = list(actions)
        # if state.count(0) == 12:
            # print ('endgame has started')
            # depth = 7
        while True:
            depth = depth + 1
            values = {}
            alpha = float('-inf')
            beta = float('inf')
            # state_id = 0
            for action in sorted_actions:
                x,y,p = action
                if (x==0 and y==0) or (x==7 and y==7) or (x==7 and y==0) or (x==0 and y==7):
                    values[action] = 8000
                else:
                    succesor_state = state.successor(action)
                    # state_id = convert_state(succesor_state)
                    # if state_id in visited_states:
                    #     values[action] = visited_states[state_id]
                    #     # print (f'found a state {state_id} = {values[action]}')
                    # else:
                    values[action] = self.min_value(succesor_state, state, depth - 1, alpha, beta)
            max_value = max(values.values())
            candidates = [action for action in actions if (values[action] - max_value > -1)]
            selected_candidate = random.choice(candidates)
            # sort actions according to their pay-off
            sorted_actions = ()
            sorted_actions = sorted(values, key=values.get, reverse=True)
            # print()
            # print (depth)
            # print (max_value)
            # print (selected_candidate)
            # print(sorted_actions)
            # state.successor(action).printstate()
            # if state.count(0) > 30 and state.count(0) < 40:
            # print(state.grid)

            # if state.count(0) == 28:
            #     print(values) 
            #     print(sorted_actions)
            # exit endgame before all states are explored, heuristics becomes useless when all actions result in value = 10000
            # if depth > 1 and depth < 16:
            #     print (depth)
            #     print (max_value)
            #     print (selected_candidate)
                # state.successor(action).printstate()
            if depth + 1 == state.count(0):
                yield selected_candidate
                # print ('early break')
                break
            # return  best action from the best depth reached
            yield selected_candidate

    def max_value(self, state, prevstate, depth, alpha, beta):
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
        global prunecount 
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
                    return self.min_value(OthelloState(state), state, depth - 1, alpha, beta)
        if depth == 0:
            # return state.count(state.player)
            return heuristics(state, prevstate, state.player, self.weights)
        value = float('-inf')
        for action in actions:
            succesor_state = state.successor(action)
            # state_id = convert_state(succesor_state)
            # if state_id in visited_states:
            #     value = visited_states[state_id]
            #     # print (f'found a state {state_id} = {value}')
            # else:
            value = max(value, self.min_value(succesor_state, state, depth - 1, alpha, beta))
            alpha = max(value, alpha)
            if beta <= alpha:
                prunecount = prunecount + 1
                # print(f"tree pruned: {prunecount}")
                break
        return value

    def min_value(self, state, prevstate, depth, alpha, beta):
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
        global prunecount 
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
                    return self.max_value(OthelloState(state), state, depth - 1, alpha, beta)
        if depth == 0:
            # return state.count(3 - state.player)
            return heuristics(state, prevstate, 3 - state.player, self.weights)
        value = float('inf')
        for action in actions:
            succesor_state = state.successor(action)
            # state_id = convert_state(succesor_state)
            # if state_id in visited_states:
            #     value = visited_states[state_id]
            #     # print (f'found a state {state_id} = {value}')
            # else:
            value = min(value, self.max_value(succesor_state, state, depth - 1, alpha, beta))
            beta = min(value, beta)
            if beta <= alpha:
                prunecount = prunecount + 1
                # print(f"tree pruned: {prunecount}")
                break
        return value

def convert_state(state):
    board = state.grid
    hash_value = state.player * 10 ** 65
    for i in range(64):
        hash_value = hash_value + board[i] * (10 ** (64-i))
    return hash_value


def heuristics(state, prevstate, player, weights):
    board = state.grid
    board_opponent = prevstate.grid
    # board = [2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 1, 2, 1, 2, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
    opponent = 3-player
    value_board = 0
    corner_count = 0
    temp_square_weights = list(square_weights)
    # check corners
    for corner in corners.keys():
        if board[corner] == player:
            corner_count += 1
            for square, value in corners[corner]:
                temp_square_weights[square] = value
        elif board[corner] == opponent:
            corner_count -= 1
    # evaluate board
    for i in range(63):
        if board[i] == player:
            value_board += temp_square_weights[i]
        elif board[i] == opponent:
            value_board -= temp_square_weights[i]
    
    # check mobility
    possible_moves_player = list()
    possible_moves_opponent = list()
    mobility = 0
    possible_moves_player = state.actions()
    # state_copy = OthelloState(state)
    possible_moves_opponent = prevstate.actions()
    mobility = len(possible_moves_player) - len(possible_moves_opponent)
    
    # check potential mobility
    potential_moves_player = 0
    potential_moves_opponent = 0
    potential_mobility = 0

    # for i in range(9,55):
    #     if board[i] == 0:
    #         if i % 8 == 0: continue # discarding edges
    #         if i % 8 == 7: continue # discarding edges
    #         for square in neighbour_squares:
    #             if board[i+square] == opponent:
    #                 potential_moves_player = potential_moves_player + 1
    #             elif board[i+square] == player:
    #                 potential_moves_opponent = potential_moves_opponent + 1
    # potential_mobility = potential_moves_player - potential_moves_opponent

    for i in range(9,55):
        if board[i] == 0:
            if i % 8 == 0: continue # discarding edges
            if i % 8 == 7: continue # discarding edges
            for square in neighbour_squares:
                if board[i+square] == opponent:
                    potential_moves_player = potential_moves_player + 1
                
    for i in range(9,55):
        if board_opponent[i] == 0:
            if i % 8 == 0: continue # discarding edges
            if i % 8 == 7: continue # discarding edges
            for square in neighbour_squares:
                if board[i+square] == player:
                    potential_moves_opponent = potential_moves_opponent + 1
    
    potential_mobility = potential_moves_player - potential_moves_opponent


    # coin parity
    coins_player = state.count(player)
    coins_opponent = state.count(opponent)
    coins = coins_player - coins_opponent
    if state.count(0) < 10: 
        weight_coins = 60
    else:
        weight_coins = 5

    # coin flip
    coinflip = coins_player - prevstate.count(opponent)
    if state.count(0) < 10: 
        weight_flip = 60
    else:
        weight_flip = -5
    

    # add all values together
    heuristic = weights[0] * corner_count + weights[1]*value_board + weights[2] * mobility + weights[3] * potential_mobility + weight_coins * coins + weight_flip * coinflip
    
    # add state to visited state dictionary
    # state_id = convert_state(state)
    # visited_states[state_id] = heuristic
    return heuristic