from numpy import loadtxt
from sklearn.model_selection import train_test_split
from sklearn.tree.tree import DecisionTreeClassifier

func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[:, -1]
data = all_data[:, 0:-1]
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=100)

# SEIF A -  Train the tree without trimming
clf = DecisionTreeClassifier(criterion="entropy")
clf.fit(train_x, train_y)
success_rate = clf.score(test_x, test_y)

# SEIF B - Trim to leaves smaller or equal to 20
clf = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=20)
clf.fit(train_x, train_y)
success_rate = clf.score(test_x, test_y)
