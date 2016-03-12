import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from pymongo import Connection
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

stemmer = SnowballStemmer('english')


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (stemmer.stem(w) for w in analyzer(doc))


def load_data(label=None):
    c = Connection(host='localhost', port=27017)
    db = c.sentweet
    sentences = []
    y = []
    if label is not None:
        sentiments = db.sentiments.find({'emotion': {'$in': label}})
    else:
        sentiments = db.sentiments.find()
    for row in sentiments:
        sentences.append(row['sentence'].translate(dict((ord(char), None) for char in "1234567890'")).rstrip('\n'))
        y.append(row['emotion'])
    return sentences, y

    
def plot_confusion_matrix(cm, label, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(label))
    plt.xticks(tick_marks, label, rotation=45)
    plt.yticks(tick_marks, label)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    
def visualize_dataset(X, y, label):
    svd = TruncatedSVD(n_components=2, algorithm='arpack').fit(X)
    reduced_X = svd.transform(X)
    colors = {0: 'r', 1: 'b', 2: 'g', 3: 'w', 4: 'c', 5: 'm', 6: 'k'}
    
    Point = namedtuple('Point', 'x y')

    data = {}
    for l in label:
        data[l] = Point([], [])
    for i in range(len(reduced_X)):
        for l in label:
            if y[i] == l:
                data[l].x.append(reduced_X[i][0])
                data[l].y.append(reduced_X[i][1])
                
    for k, l in enumerate(label):
        plt.scatter(data[l].x, data[l].y, c=colors[k], marker='o')
    plt.legend(label, loc=2)