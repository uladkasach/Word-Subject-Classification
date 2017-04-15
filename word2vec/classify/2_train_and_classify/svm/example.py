#https://www.safaribooksonline.com/library/view/tensorflow-machine-learning/9781786462169/ch04s05.html
#http://scikit-learn.org/stable/modules/svm.html

from sklearn import svm
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
print(clf);
result = clf.fit(X, y);
print(result);

'''
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
'''

result = clf.predict([[2., 2.]])
print(result);


