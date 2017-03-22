from sklearn import svm
import numpy;
from sklearn import datasets;
import matplotlib.pyplot as plt;
Xi, yi = datasets.make_blobs(500, random_state=1111);
print(yi[0:10]);
Xi = Xi.astype(numpy.float32)
the_data = Xi;
K = 3;
#print(the_data);



clf = svm.SVC()
clf.fit(Xi, yi);

'''
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
'''

assignments = clf.predict(Xi)
print(assignments);

'''
vectors = clf.support_vectors_
print(vectors);
'''


plt.scatter(*Xi.T, c='k', lw=0);
plt.scatter(*Xi.T, c=yi, lw=0, vmax=K + 0.5, label='data');
plt.legend(scatterpoints=3);
plt.show()
        