import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS, O_PLAYER, X_PLAYER, NUM_OF_MOVES_IN_OPENING_BOOK, \
    TIE
import time
import copy
import pickle
from collections import defaultdict

class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.time()
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

        with open('opening_book_better.pkl', 'rb') as source:
            self.opening_book = pickle.load(source)

        self.last_board = []
        for i in range(BOARD_COLS):
            self.last_board.append([EM] * BOARD_ROWS)

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                self.last_board[x][y] = EM

        # Starting pieces:
        self.last_board[3][3] = X_PLAYER
        self.last_board[3][4] = O_PLAYER
        self.last_board[4][3] = O_PLAYER
        self.last_board[4][4] = X_PLAYER

        self.moves = ""

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), '- better_player')

    def find_oposit_move(self, game_state):
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS):
                if self.last_board[i][j] == EM and game_state.board[i][j] != EM:
                    return i, j
        return None

    def opening_move(self, game_state):
        if len(self.moves)/2 > NUM_OF_MOVES_IN_OPENING_BOOK:
            return None
        other_player_move = self.find_oposit_move(game_state)
        if other_player_move is None:
            other_player_move_as_str = ""
        else:
            other_player_move_as_str = xy_to_a1(other_player_move)
        self.moves += other_player_move_as_str

        return a1_to_xy(self.opening_book[self.moves]) if self.moves in self.opening_book else None

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        best_move = self.opening_move(game_state)

        if best_move is None:
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

        game_state.perform_move(best_move[0], best_move[1])
        self.last_board = game_state.board

        self.moves += xy_to_a1(best_move)

        return best_move

    def utility(self, state):
        if len(state.get_possible_moves()) == 0:
            winner = state.get_winner()
            if winner == self.color:
                return INFINITY
            elif winner == TIE:
                return 0
            else:
                return -INFINITY

        my_in_corner = 0
        opp_in_corner = 0
        my_front = 0
        opp_front = 0
        my = 0
        opp = 0
        d = 0
        my_close_to_corner = 0
        opp_close_to_corner = 0
        close_to_corner = 0
        opp_state = copy.deepcopy(state)
        X = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y = [0, 1, 1, 1, 0, -1, -1, -1]
        piece_diff = [[0]*BOARD_ROWS]*BOARD_COLS
        piece_diff[0] = [20, -3, 11, 8, 8, 11, -3, 20]
        piece_diff[1] = [-3, -7, -4, 1, 1, -4, -7, -3]
        piece_diff[2] = [11, -4, 2, 2, 2, 2, -4, 11]
        piece_diff[3] = [8, 1, 2, -3, -3, 2, 1, 8]
        piece_diff[4] = [8, 1, 2, -3, -3, 2, 1, 8]
        piece_diff[5] = [11, -4, 2, 2, 2, 2, -4, 11]
        piece_diff[6] = [-3, -7, -4, 1, 1, -4, -7, -3]
        piece_diff[7] = [20, -3, 11, 8, 8, 11, -3, 20]
        if state.curr_player == X_PLAYER:
            opp_state.curr_player = O_PLAYER
        else:
            opp_state.curr_player = X_PLAYER

        grid = state.board
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if grid[x][y] == self.color:
                    my += 1
                    d += piece_diff[x][y]
                elif grid[x][y] == OPPONENT_COLOR[self.color]:
                    opp += 1
                    d -= piece_diff[x][y]
                if grid[x][y] != ' ':
                    for k in range(BOARD_ROWS):
                        i = x+X[k]
                        j = y+Y[k]
                        if i >= 0 and i < BOARD_ROWS and j >= 0 and j < BOARD_ROWS and grid[i][j] == EM:
                            if grid[x][y] == self.color:
                                my_front += 1
                            elif grid[x][y] == OPPONENT_COLOR[self.color]:
                                opp_front += 1
                            break

        if my_front > opp_front:
            front = -(100.0 * my_front)/(my_front + opp_front)
        elif my_front < opp_front:
            front = (100.0 * opp_front) / (my_front + opp_front)
        else:
            front = 0

        if my > opp:
            tiles = (100.0 * my)/(my + opp)
        elif my < opp:
            tiles = -(100.0 * opp)/(my + opp)
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

        corners = 25 * (my_in_corner - opp_in_corner)
        my_options = len(state.get_possible_moves())
        opp_options = len(opp_state.get_possible_moves())

        if my_options > opp_options:
            options = (100.0 * my_options)/(my_options + opp_options)
        elif opp_options > my_options:
            options = -(100.0 * opp_options)/(my_options + opp_options)
        else:
            options = 0

        if grid[0][0] == EM:
            if grid[0][1] == self.color:
                my_close_to_corner += 1
            elif grid[0][1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[1][1] == self.color:
                my_close_to_corner += 1
            elif grid[1][1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[1][0] == self.color:
                my_close_to_corner += 1
            elif grid[1][0] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
        if grid[0][BOARD_COLS-1] == EM:
            if grid[0][BOARD_COLS-2] == self.color:
                my_close_to_corner += 1
            elif grid[0][BOARD_COLS-2] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[1][BOARD_COLS-2] == self.color:
                my_close_to_corner += 1
            elif grid[1][BOARD_COLS-2] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[1][BOARD_COLS-1] == self.color:
                my_close_to_corner += 1
            elif grid[1][BOARD_COLS-1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
        if grid[BOARD_ROWS-1][0] == EM:
            if grid[BOARD_ROWS-1][1] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-1][1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[BOARD_ROWS-2][1] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-2][1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[BOARD_ROWS-2][0] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-2][0] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
        if grid[BOARD_ROWS-1][BOARD_COLS-1] == EM:
            if grid[BOARD_ROWS-2][BOARD_COLS-1] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-2][BOARD_COLS-1] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[BOARD_ROWS-2][BOARD_COLS-2] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-2][BOARD_COLS-2] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1
            if grid[BOARD_ROWS-1][BOARD_COLS-2] == self.color:
                my_close_to_corner += 1
            elif grid[BOARD_ROWS-1][BOARD_COLS-2] == OPPONENT_COLOR[self.color]:
                opp_close_to_corner += 1

        close_to_corner = -12.5 * (my_close_to_corner - opp_close_to_corner)

        score = (10 * tiles) + (801.724 * corners) + (382.026 * close_to_corner) + (78.922 * options) + (74.396 * front)\
               + (10 * d)

        return score


def xy_to_a1(move):
    return chr(ord('a') + (7-int(move[0]))) + str(int(move[1]) + 1)


def a1_to_xy(move):
    return 7-(ord(move[0]) - ord('a')), int(move[1]) - 1

