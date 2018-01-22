import pandas as pd
from sklearn.ensemble import RandomForestRegressor

#import data set and test set
data_set = pd.read_csv('diamonds.csv')
test_set = pd.read_csv('unlabeled_diamonds.csv')

# create maps form feature to number, save on the orders betwenn each feature
clarity_map = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}
cut_map = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
color_map = {'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 4, 'I': 5, 'J': 6}

# create map from the number to the feature string
rev_clarity_map = {val: key for key, val in clarity_map.items()}
rev_cut_map = {val: key for key, val in cut_map.items()}
rev_color_map = {val: key for key, val in color_map.items()}

# create data set with only numbers, base on the maps
data_set['cut'] = data_set['cut'].map(lambda x: cut_map[x])
data_set['color'] = data_set['color'].map(lambda x: color_map[x])
data_set['clarity'] = data_set['clarity'].map(lambda x: clarity_map[x])

# create test set with only numbers, base on the maps
test_set['cut'] = test_set['cut'].map(lambda x: cut_map[x])
test_set['color'] = test_set['color'].map(lambda x: color_map[x])

# create train set(x) without the clrity and train set (y) with only clarity
train_y = data_set.pop('clarity').values
train_x = data_set.values

# create the test (x)
test_x = test_set.values

# create the random forest regressor with 100 trees and fit him
rf = RandomForestRegressor(n_estimators=100)
rf.fit(train_x, train_y)

# find the prediction on test and round the pred to get int
pred = rf.predict(test_x)
round_pred = [round(p) for p in pred]

# add the prediction to the test set
test_set.insert(4, 'clarity', round_pred)

# change the numbers to string of the features based on the maps
test_set['cut'] = test_set['cut'].map(lambda x: rev_cut_map[x])
test_set['color'] = test_set['color'].map(lambda x: rev_color_map[x])
test_set['clarity'] = test_set['clarity'].map(lambda x: rev_clarity_map[x])

# write new lable diamonds based on the unlable and the our prediction
headr = ['carat','cut','color','clarity','depth','table','price','x','y','z']
test_set.to_csv('labeled_diamonds.csv', columns=headr)

