from emnist import extract_training_samples as em
from builtins import range, input

import numpy as np
from datetime import datetime
from scipy.stats import norm
from scipy.stats import multivariate_normal as mvn

# utils import load_images

def load_images():
    images, labels = em('byclass')

    return images, labels

class NaiveBayes(object):
    def fit(self, X, Y, smoothing=1e-2):
        self.gaussians = dict()
        self.priors = dict()
        labels = set(Y)
        for c in labels:
            current_x = X[Y == c]
            self.gaussians[c] = {
                'mean': current_x.mean(axis=0),
                'var': current_x.var(axis=0) + smoothing,
            }
            self.priors[c] = float(len(Y[Y == c])) / len(Y)

    def score(self, X, Y):
        P = self.predict(X)
        return np.mean(P == Y)

    def predict(self, X):
        N, D = X.shape
        K = len(self.gaussians)
        P = np.zeros((N, K))
        for c, g in self.gaussians.items():
            mean, var = g['mean'], g['var']
            P[:,c] = mvn.logpdf(X, mean=mean, cov=var) + np.log(self.priors[c])
        return np.argmax(P, axis=1)

images, labels = load_images()
numImages = len(labels)
Ntrain = numImages // 2
counter = 0

new_images = np.zeros((numImages,784))
for image in images: 
  new_image  = image.flatten()
  new_images[counter] = new_image
  counter +=1

Ntrain = len(labels) // 2
Xtrain, Ytrain = new_images[:Ntrain], labels[:Ntrain]
Xtest, Ytest = new_images[Ntrain:], labels[Ntrain:]

Xtrain.shape

model = NaiveBayes()
model.fit(Xtrain,Ytrain)
print("Train accuracy:", model.score(Xtrain, Ytrain))
print("Test accuracy:", model.score(Xtest, Ytest))

