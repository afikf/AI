import numpy as np
from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


func = lambda x: 0.0 if x == b'False' else 1.0
all_data = loadtxt('flare.csv', delimiter=',', skiprows=1, converters={32: func})
target = all_data[: , -1]
data = all_data[:, 0:-1]
clf = DecisionTreeClassifier(criterion="entropy")
succ_rate = cross_val_score(clf, data, target, cv=4)
target_predict = cross_val_predict(clf, data, target, cv=4)
succ_rate_avg = np.average(succ_rate)
conf_mat = confusion_matrix(target, target_predict)
labels = ('True Negative', 'False Positive', 'False Negative', 'True Positive')
y_pos = np.arange(len(labels))
results = (conf_mat.reshape((1, 4))).tolist()[0]
plt.bar(y_pos, results, align='center', alpha=0.5)
plt.xticks(y_pos, labels)
plt.title('Confusion Matrix')
print(succ_rate_avg)
print(conf_mat)
plt.figure()
class_names = ['True', 'False']
plot_confusion_matrix(conf_mat, classes=class_names,
                      title='Confusion matrix, without normalization')
plt.show()

a=DecisionTreeClassifier()
a.fit()





