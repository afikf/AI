import numpy as np
from matplotlib import pyplot as plt


def calculateProb(x_, t, array):
    return x_**(-1/t)/sum([x_i**(-1/t) for x_i in array])

colors = ['red', 'blue', 'green', 'orange', 'grey']
X = np.array([400, 900, 390, 1000, 550])

T = np.linspace(0.01, 5, 100, endpoint=True)

result = []
alpha = min(X)
plt.figure()
for idx, x in enumerate(X):
    alpha = min(calculateProb(x, T, X))
    plt.plot(T, calculateProb(x/alpha, T, X/alpha), color=colors[idx], label=str(x))

plt.legend()

plt.show()
