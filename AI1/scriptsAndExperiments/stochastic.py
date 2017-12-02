from consts import Consts
from astar import AStar
from ways import load_map_from_csv
from busSolvers import GreedyBestFirstSolver, GreedyStochasticSolver
from problems import BusProblem
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic
import numpy as np
import scipy as sp
from scipy import stats

REPEATS = 150

# Load the files
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
prob = BusProblem.load(Consts.getDataFilePath("HAIFA_100.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

scorer = L2DistanceCost(roads)

# Run the greedy solver
pickingPath = GreedyBestFirstSolver(roads, mapAstar, scorer).solve(prob)
greedyDistance = pickingPath.getDistance() / 1000
print("Greedy solution: {:.2f}km".format(greedyDistance))

# Run the stochastic solver #REPATS times
solver = GreedyStochasticSolver(roads, mapAstar, scorer,
                                Consts.STOCH_INITIAL_TEMPERATURE,
                                Consts.STOCH_TEMPERATURE_DECAY_FUNCTION,
                                Consts.STOCH_TOP_SCORES_TO_CONSIDER)
results = np.zeros((REPEATS,))
results_for_graph = results.copy()
print("Stochastic repeats:")
for i in range(REPEATS):
    print("{}..".format(i+1), end=" ", flush=True)
    results[i] = solver.solve(prob).getDistance() / 1000
    # Take only the lower values to the graph
    results_for_graph[i] = results[i] if i == 0 or results[i] < results_for_graph[i-1] else results_for_graph[i-1]

print("\nDone!")

# TODO : Part1 - Plot the diagram required in the instructions
from matplotlib import pyplot as plt

plt.figure()

plt.plot(np.arange(0, REPEATS, 1), results_for_graph, 'blue', label="Greedy Stochastic")
plt.plot(np.arange(0, REPEATS, 1), [greedyDistance]*REPEATS, 'yellow', label="Greedy Best First")

plt.legend()
plt.grid()

plt.title("Stochastic and Determinist greedy solvers")
plt.xlabel("Iterations")
plt.ylabel("Total path length")

plt.show()

# TODO : Part2 - Remove the exit and perform the t-test

# Calculate average and standard deviation
averageRes = np.average(results)
standardDevRes = np.std(results)

print("Average of x_i is {:e}\nStandart deviation of x_i is {:e}\n".format(averageRes, standardDevRes))

# Run the t-test
statistic, p_value = stats.ttest_1samp(results, greedyDistance)

print("p-value is {:e}\n".format(p_value))
