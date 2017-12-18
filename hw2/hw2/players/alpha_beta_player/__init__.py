import time

from abstract import AbstractPlayer
from utils import MiniMaxWithAlphaBetaPruning
from players.better_player import Player as simplePlayer
from players.min_max_player import Player as min_max_player

INFINITY = float(6000)

class Player(AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)

        self.clock = time.time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

        self.simple = simplePlayer(setup_time, player_color, time_per_k_turns, k)
        self.min_max = min_max_player(setup_time, player_color, time_per_k_turns, k)

        self.algorithm = MiniMaxWithAlphaBetaPruning(utility=self.simple.utility, my_color=self.color,
                                     no_more_time=self.min_max.no_more_time, selective_deepening=self.alwaysTrue)

    def alwaysTrue(self, state):
        return True

    def get_move(self, game_state, possible_moves):
        depth = 0
        self.time_for_current_move = self.min_max.time_for_step()
        self.clock = time.time()

        best_move = None
        max_value = 0
        reached_leaves = False
        while not self.min_max.no_more_time() and not reached_leaves:
            depth += 1
            [value, move, reached_leaves] = self.algorithm.search(game_state, depth, -INFINITY, INFINITY, True)
            if best_move is None or value > max_value:
                max_value = value
                best_move = move

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1

        return best_move if best_move is not None else possible_moves[0]
