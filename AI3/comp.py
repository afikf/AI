import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import random
import numpy as np

data_set = pd.read_csv('diamonds.csv')
test_set = pd.read_csv('unlabeled_diamonds.csv')
clarity_map = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}
cut_map = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
color_map = {'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 4, 'I': 5, 'J': 6}
rev_clarity_map = {val: key for key, val in clarity_map.items()}
rev_cut_map = {val: key for key, val in cut_map.items()}
rev_color_map = {val: key for key, val in color_map.items()}
data_set['cut'] = data_set['cut'].map(lambda x: cut_map[x])
data_set['color'] = data_set['color'].map(lambda x: color_map[x])
data_set['clarity'] = data_set['clarity'].map(lambda x: clarity_map[x])
test_set['cut'] = test_set['cut'].map(lambda x: cut_map[x])
test_set['color'] = test_set['color'].map(lambda x: color_map[x])
# rows = data_set.index
# row_count = len(rows)
# random.shuffle(list(rows))
#
# data_set.reindex(rows)
#
# training_data = data_set[row_count // 10:]
# testing_data = data_set[:row_count // 10]
train_y = data_set.pop('clarity').values
train_x = data_set.values

test_x = test_set.values

rf = RandomForestRegressor(n_estimators=100)
rf.fit(train_x, train_y)
pred = rf.predict(test_x)
round_pred = [round(p) for p in pred]
test_set.insert(4, 'clarity', round_pred)
test_set['cut'] = test_set['cut'].map(lambda x: rev_cut_map[x])
test_set['color'] = test_set['color'].map(lambda x: rev_color_map[x])
test_set['clarity'] = test_set['clarity'].map(lambda x: rev_clarity_map[x])
headr = ['carat','cut','color','clarity','depth','table','price','x','y','z']
test_set.to_csv('labeled_diamonds.csv', columns=headr)
a=1
