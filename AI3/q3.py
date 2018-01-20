import numpy as np
from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
from  sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix


func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[: , -1]
data = all_data[:, 0:-1]

train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=100)

# under fitting
under_clf = DecisionTreeClassifier(max_depth=1)
under_clf.fit(train_x, train_y)
under_train_succ_rate = under_clf.score(train_x, train_y)
under_test_succ_rate = under_clf.score(test_x, test_y)


print(under_train_succ_rate)

# over fitting
over_clf = DecisionTreeClassifier()
over_clf.fit(train_x, train_y)
over_train_succ_rate = over_clf.score(train_x, train_y)
over_test_succ_rate = over_clf.score(test_x, test_y)

print(over_train_succ_rate)

