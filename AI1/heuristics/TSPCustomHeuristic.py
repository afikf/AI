from heuristics import Heuristic
from ways.tools import compute_distance
# TODO : Implement as explained in the instructions
class TSPCustomHeuristic(Heuristic):
    _distMat = {}
    _junctionToMatIdx = None

    # TODO : You can add parameters if you need them
    def __init__(self, roads, initialState):
        super().__init__()
        self._roads = roads

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    def estimate(self, problem, state):
        waitingList = state.waitingOrders

        if len(waitingList) == 0:
            return 0

        def compute(order):
            if (state.junctionIdx, order[0]) in self._distMat:
                return self._distMat[(state.junctionIdx, order[0])]
            else:
                dist = compute_distance(self._roads[state.junctionIdx].coordinates, self._roads[order[0]].coordinates)
                self._distMat[(state.junctionIdx, order[0])] = dist
                return dist

        # Find the order with the maximal aerial distance from the current state to starting point
        max_dist_order = max(waitingList, key=compute)

        # Return the distance itself (already cached)
        return self._distMat[(state.junctionIdx, max_dist_order[0])]

