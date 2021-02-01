# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
import numpy as np
import sys
import math
def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    W = np.zeros(len(train_set[0]))
    b = 0
    for j in range(max_iter):
        done = True
        for i in range(len(train_set)):
            curr_image = train_set[i]
            label = train_labels[i]
            y = -1
            ystar = -1
            if label == True:
                y = 1
            if (np.dot(W, curr_image) + b) > 0:
                ystar = 1
            if (ystar > 0) != label:
                b += y*learning_rate
                W += y*learning_rate*curr_image
                done = False
        if done:
            break
                
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    ret = []
    for i in range(len(dev_set)):
        curr_image = dev_set[i]
        if (np.dot(W, curr_image) + b) > 0:
            y = 1
        else:
            y = -1
        ret.append(y > 0)
    # ret = int(ret)
    # print(ret)
    return ret

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    # try:
    ret = 1/(1 + np.exp(-x))
    return ret

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    N = len(train_labels)
    W = np.zeros(len(train_set[0])+1)
    for j in range(max_iter):
        dLdW = np.zeros(len(train_set[0])+1)
        for i in range(N):
            curr_image = train_set[i]
            curr_image = np.append(curr_image, 1)
            label = train_labels[i]
            y = 0
            if label == True:
                y = 1.0
            ystar = np.dot(W, curr_image)
            f = sigmoid(ystar)
            # print(f)
            dLdW += (f - y)*curr_image
        # print("-------------------")
        # print(learning_rate*dLdW/N)
        W -= learning_rate*dLdW/N
        # print(W)
    b = W[-1]
    # print(W)
    W = np.delete(W, -1)
    # print(W)
    return W, b

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    # np.set_printoptions(threshold=sys.maxsize)
    W, b = trainLR(train_set, train_labels, learning_rate, max_iter)
    # val = W
    # print(val)
    # print(b)
    ret = []
    for i in range(len(dev_set)):
        curr_image = dev_set[i]
        ret.append(sigmoid(np.dot(W, curr_image) + b) > 0.5)
    # ret = int(ret)
    # print(ret)
    return ret

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    return []
