from . import Heuristic
from costs import L2DistanceCost
from problems import MapProblem

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        # TODO : Return the correct distance
        target_state = MapProblem(problem).target
        return L2DistanceCost(problem._roads).compute(state, target_state)

