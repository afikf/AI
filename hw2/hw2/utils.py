"""Generic utility functions
"""
# from __future__ import print_function
from threading import Thread
from multiprocessing import Queue
import time
import copy

INFINITY = float(6000)


class ExceededTimeError(RuntimeError):
    """Thrown when the given function exceeded its runtime.
    """
    pass


def function_wrapper(func, args, kwargs, result_queue):
    """Runs the given function and measures its runtime.

    :param func: The function to run.
    :param args: The function arguments as tuple.
    :param kwargs: The function kwargs as dict.
    :param result_queue: The inter-process queue to communicate with the parent.
    :return: A tuple: The function return value, and its runtime.
    """
    start = time.time()
    try:
        result = func(*args, **kwargs)
    except MemoryError as e:
        result_queue.put(e)
        return

    runtime = time.time() - start
    result_queue.put((result, runtime))


def run_with_limited_time(func, args, kwargs, time_limit):
    """Runs a function with time limit

    :param func: The function to run.
    :param args: The functions args, given as tuple.
    :param kwargs: The functions keywords, given as dict.
    :param time_limit: The time limit in seconds (can be float).
    :return: A tuple: The function's return value unchanged, and the running time for the function.
    :raises PlayerExceededTimeError: If player exceeded its given time.
    """
    q = Queue()
    t = Thread(target=function_wrapper, args=(func, args, kwargs, q))
    t.start()

    # This is just for limiting the runtime of the other thread, so we stop eventually.
    # It doesn't really measure the runtime.
    t.join(time_limit)

    if t.is_alive():
        raise ExceededTimeError

    q_get = q.get()
    if isinstance(q_get, MemoryError):
        raise q_get
    return q_get


class MiniMaxAlgorithm:

    def __init__(self, utility, my_color, no_more_time, selective_deepening):
        """Initialize a MiniMax algorithms without alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        :param selective_deepening: A functions that gets the current state, and
                        returns True when the algorithm should continue the search
                        for the minimax value recursivly from this state.
                        optional
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.selective_deepening = selective_deepening

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The move in case of max node or None in min mode)
        """

        possible_moves = state.get_possible_moves()

        # Check if we need to end the game. The game will be ended if:
        # 1. It is a goal state
        # 2. Out of time
        # 3. It is selective depth game, stop if it is too deep
        # 4. No possible moves
        if not self.selective_deepening(state) or self.no_more_time() or depth == 0 or 0 == len(possible_moves):
            return [self.utility(state), None, True] if 0 == len(possible_moves) else [self.utility(state), None, False]

        reached_leaves = True
        if maximizing_player:
            cur_max = -1*INFINITY
            max_move = None
            for move in possible_moves:
                next_state = copy.deepcopy(state)
                next_state.perform_move(move[0], move[1])
                [value, _, cur_reached_leaves] = self.search(next_state, depth - 1, False)
                reached_leaves = reached_leaves and cur_reached_leaves
                if value > cur_max:
                    cur_max = value
                    max_move = move
            return cur_max, max_move, reached_leaves

        # minimizing player
        cur_min = INFINITY
        for move in possible_moves:
            next_state = copy.deepcopy(state)
            next_state.perform_move(move[0], move[1])
            [value, _, cur_reached_leaves] = self.search(next_state, depth - 1, True)
            reached_leaves = reached_leaves and cur_reached_leaves
            cur_min = min(cur_min, value)
        return cur_min, None, reached_leaves

class MiniMaxWithAlphaBetaPruning:

    def __init__(self, utility, my_color, no_more_time, selective_deepening):
        """Initialize a MiniMax algorithms with alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        :param selective_deepening: A functions that gets the current state, and
                        returns True when the algorithm should continue the search
                        for the minimax value recursivly from this state.
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.selective_deepening = selective_deepening

    def search(self, state, depth, alpha, beta, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param alpha: The alpha of the alpha-beta pruning.
        :param beta: The beta of the alpha-beta pruning.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The alpha-beta algorithm value, The move in case of max node or None in min mode)
        """

        possible_moves = state.get_possible_moves()

        # Check if we need to end the game. The game will be ended if:
        # 1. It is a goal state
        # 2. Out of time
        # 3. It is selective depth game, stop if it is too deep
        # 4. No possible moves
        if not self.selective_deepening(state) or self.no_more_time() or depth == 0 or 0 == len(possible_moves):
            return [self.utility(state), None, True] if 0 == len(possible_moves) else [self.utility(state), None, False]

        reached_leaves = True
        if maximizing_player:
            cur_max = -1*INFINITY
            max_move = None
            for move in possible_moves:
                next_state = copy.deepcopy(state)
                next_state.perform_move(move[0], move[1])
                [value, _, cur_reached_leaves] = self.search(next_state, depth - 1, alpha, beta, False)
                reached_leaves = reached_leaves and cur_reached_leaves
                if value > cur_max:
                    cur_max = value
                    max_move = move
                alpha = max(cur_max, alpha)
                if cur_max >= beta:
                    return INFINITY, move, reached_leaves
            return cur_max, max_move, reached_leaves

        # minimizing player
        cur_min = INFINITY
        for move in possible_moves:
            next_state = copy.deepcopy(state)
            next_state.perform_move(move[0], move[1])
            [value, _, cur_reached_leaves] = self.search(next_state, depth - 1, alpha, beta, True)
            cur_min = min(cur_min, value)
            beta = min(cur_min, beta)
            reached_leaves = reached_leaves and cur_reached_leaves
            if cur_min <= alpha:
                return -INFINITY, None, reached_leaves
        return cur_min, None, reached_leaves
