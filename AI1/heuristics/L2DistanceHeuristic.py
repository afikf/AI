from . import Heuristic
from costs import L2DistanceCost
from problems import MapProblem
from ways.tools import compute_distance

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        target_state = problem.target
        # Return the aerial distance between the state and the target
        return compute_distance(state.coordinates, target_state.coordinates)

