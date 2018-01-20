import numpy as np

def sfs(x, y, k, clf, score):
    """
    :param x: feature set to be trained using clf. list of lists.
    :param y: labels corresponding to x. list.
    :param k: number of features to select. int
    :param clf: classifier to be trained on the feature subset.
    :param score: utility function for the algorithm, that receives clf, feature subset and labeles, returns a score. 
    :return: list of chosen feature indexes
    """
    if k == 0:
        return []

    indices = sfs(x, y, k - 1, clf, score)

    max_utility = None
    max_index = 0

    for index in range(len(x[0])):
        if index in indices:
            continue

        samples = np.asarray(x)
        samples = samples[:, indices + [index]]
        utility = score(clf, samples, y)

        if utility > max_utility:
            max_utility = utility
            max_index = index

    return indices + [max_index]
