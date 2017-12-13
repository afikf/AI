import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS, O_PLAYER, X_PLAYER
import time
import copy
from collections import defaultdict

class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.time()
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better')

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        best_move = possible_moves[0]
        next_state = copy.deepcopy(game_state)
        next_state.perform_move(best_move[0], best_move[1])
        # Choosing an arbitrary move
        # Get the best move according the utility function
        for move in possible_moves:
            new_state = copy.deepcopy(game_state)
            new_state.perform_move(move[0], move[1])
            if self.utility(new_state) > self.utility(next_state):
                next_state = new_state
                best_move = move

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        return best_move

    def utility(self, state):
        if len(state.get_possible_moves()) == 0:
            return INFINITY if state.curr_player != self.color else -INFINITY
        my_in_corner = 0
        opp_in_corner = 0
        my = 0
        opp = 0
        opp_state = copy.deepcopy(state)
        if state.curr_player == X_PLAYER:
            opp_state.curr_player = O_PLAYER
        else:
            opp_state.curr_player = X_PLAYER

        grid = state.board

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if grid[x][y] == self.color:
                    my += 1
                elif grid[x][y] == OPPONENT_COLOR[self.color]:
                    opp += 1

        if my > opp:
            tiles = my
        elif my < opp:
            tiles = -opp
        else:
            tiles = 0

        if grid[0][0] == self.color:
            my_in_corner += 1
        elif grid[0][0] == OPPONENT_COLOR[self.color]:
            opp_in_corner += 1
        if grid[0][BOARD_ROWS-1] == self.color:
            my_in_corner += 1
        elif grid[0][BOARD_ROWS-1] == OPPONENT_COLOR[self.color]:
            opp_in_corner += 1
        if grid[BOARD_COLS-1][0] == self.color:
            my_in_corner += 1
        elif grid[BOARD_COLS-1][0] == OPPONENT_COLOR[self.color]:
            opp_in_corner += 1
        if grid[BOARD_COLS-1][BOARD_ROWS-1] == self.color:
            my_in_corner += 1
        elif grid[BOARD_COLS-1][BOARD_ROWS-1] == OPPONENT_COLOR[self.color]:
            opp_in_corner += 1

        corners = (my_in_corner - opp_in_corner)
        my_options = len(state.get_possible_moves())
        opp_options = len(opp_state.get_possible_moves())

        if my_options > opp_options:
            options = my_options
        elif opp_options > my_options:
            options = -opp_options
        else:
            options = 0

        return corners + options + tiles



