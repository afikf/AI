from . import GreedySolver
import numpy as np

class GreedyBestFirstSolver(GreedySolver):
    def __init__(self, roads, astar, scorer):
        super().__init__(roads, astar, scorer)

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))
        max_score = 0
        bestIdx = None
        # TODO : Return the next state
        for idx, succ in enumerate(successors) :
            score = self._scorer.compute(currState, succ)
            if score > max_score:
                max_score = score
                bestIdx = idx

        if bestIdx is None:
            return None

        return successors[bestIdx]
