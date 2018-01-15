import numpy as np
from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix

func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[: , -1]
data = all_data[:, 0:-1]
clf = DecisionTreeClassifier(criterion="entropy")
succ_rate = cross_val_score(clf, data, target, cv=4)
target_predict = cross_val_predict(clf, data, target, cv=4)
succ_rate_avg = np.average(succ_rate)
conf_mat = confusion_matrix(target, target_predict)
print(succ_rate_avg)
print(conf_mat)



