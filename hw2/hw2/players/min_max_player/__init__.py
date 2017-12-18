import time
from Reversi.consts import *
from abstract import AbstractPlayer
from utils import MiniMaxAlgorithm
from players.simple_player import Player as simplePlayer
import abstract

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
        self.algorithm = MiniMaxAlgorithm(utility=self.simple.utility, my_color=self.color,
                                          no_more_time=self.no_more_time, selective_deepening=self.alwaysTrue)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), '- min_max_player')

    def no_more_time(self):
        time_passed = (time.time() - self.clock)
        self.time_for_current_move -= time_passed
        self.time_remaining_in_round -= time_passed
        self.clock = time.time()
        if self.time_for_current_move <= 0.05 or self.time_remaining_in_round <= 0.05:
            return True
        return False

    def alwaysTrue(self, state):
        return True

    def time_for_step(self):
        return self.split_time_equally(PERCENTAGE_OF_TIME_TO_SPLIT_EQUALY * self.time_remaining_in_round) + \
               self.split_time_not_equally(PERCENTAGE_OF_TIME_TO_SPLIT_NOT_EQUALY * self.time_remaining_in_round) - 0.05

    def split_time_equally(self, time_remaining):
        return time_remaining/self.turns_remaining_in_round

    def split_time_not_equally(self, time_remaining):
        sum_of_remaining_turns = sum(range(self.turns_remaining_in_round + 1))
        return time_remaining * (self.turns_remaining_in_round / sum_of_remaining_turns)

    def get_move(self, game_state, possible_moves):
        depth = 0
        self.time_for_current_move = self.time_for_step()
        self.clock = time.time()

        best_move = None
        max_value = 0
        while not self.no_more_time():
            depth += 1
            [value, move, searched_all_tree] = self.algorithm.search(game_state, depth, True)
            if best_move is None or value > max_value:
                max_value = value
                best_move = move
            if searched_all_tree:
                break

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1

        return best_move if best_move is not None else possible_moves[0]

