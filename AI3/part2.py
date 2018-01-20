from numpy import loadtxt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sfs import sfs
import numpy as np
from sklearn.tree.tree import DecisionTreeClassifier

func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[:, -1]
data = all_data[:, 0:-1]
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=100)


#Seif 7:
def utility(clf, x, y):
    return clf.score(x, y)


knn = KNeighborsClassifier()
indices = sfs(train_x, train_y, 8, knn, utility)
samples = np.asarray(train_x)
samples = samples[:, indices]
test_x = test_x[:, indices]
knn.fit(samples, train_y)
score = knn.score(test_x, test_y)
print('{}'.format(score))


#Seif 8:
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=100)
clf = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=20)
clf.fit(train_x, train_y)
success_rate = clf.score(test_x, test_y)

print("{}".format(success_rate))
