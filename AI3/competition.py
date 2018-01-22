from sklearn.neural_network import MLPClassifier
from numpy import loadtxt
import numpy as np
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

cut_to_number = {}
color_to_number = {}
clarity_to_number = {}
i=0
new_rows = []

# with open('diamonds.csv', 'r') as f:
#     reader = csv.reader(f)
#     for arr in reader:
#         i+=1
#         if arr[2] not in cut_to_number and i != 1:
#             cut_to_number[arr[2]] = i
#         if arr[3] not in color_to_number and i != 1:
#             color_to_number[arr[3]] = i*5
#         if arr[4] not in clarity_to_number and i != 1:
#             clarity_to_number[arr[4]] = i*10
#
#         arr[2] = cut_to_number.get(arr[2], '')
#         arr[3] = color_to_number.get(arr[3], '')
#         arr[4] = clarity_to_number.get(arr[4], '')
#         new_rows.append(arr)
#
# with open('diamonds.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows(new_rows)
with open('diamonds.csv') as f:
    a = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
all_data = vec.fit_transform(a)
target = all_data[:, 4]

data = all_data[:, [0,1,2,3,5,6,7,8,9,10]]
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=100)

classifiers = [RandomForestClassifier(n_estimators=100, criterion='entropy', oob_score=True)]

for clf in classifiers:
    clf.fit(train_x, train_y)
    name = clf.__class__.__name__
    print("=" * 30)
    print(name)
    print('****Results****')
    train_predictions = clf.predict(test_x)
    acc = accuracy_score(test_y, train_predictions)
    print("Accuracy: {:.4%}".format(acc))
