import numpy as np
from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix


func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[: , -1]
data = all_data[:, 0:-1]

[train_x, test_x] = np.split(data, [int(0.75*data.shape[0])])
[train_y, test_y] = np.split(target, [int(0.75*target.size)])
test=1

# under fitting
under_clf = DecisionTreeClassifier(min_weight_fraction_leaf=0.5)
under_clf.fit(train_x, train_y)
under_train_succ_rate = under_clf.score(train_x, train_y)
under_test_succ_rate = under_clf.score(test_x, test_y)

print('under train succ rate is: {}'.format(under_train_succ_rate))
print('under test succ rate is: {}'.format(under_test_succ_rate))
print('\n')

# over fitting
over_clf = DecisionTreeClassifier()
over_clf.fit(train_x, train_y)
over_train_succ_rate = over_clf.score(train_x, train_y)
over_test_succ_rate = over_clf.score(test_x, test_y)

print('over train succ rate is: {}'.format(over_train_succ_rate))
print('over test succ rate is: {}'.format(over_test_succ_rate))

