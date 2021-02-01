# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """



    # TODO: Write your code here
    wordsPos = {}
    wordsNeg = {}
    ret = []
    poscount = 0
    negcount = 0
    i = 0
    # vocabSize = [0,0]

    for review in train_set:
        for word in review:
        
            if train_labels[i] == 1:
                
                try:
                    wordsPos[word] += 1
                except:
                    wordsPos[word] = 1
                    # vocabSize[1] += 1

                poscount += 1

            if train_labels[i] == 0:
                
                try:
                    wordsNeg[word] += 1
                except:
                    wordsNeg[word] = 1
                    # vocabSize[0] += 1

                negcount += 1
        
        i += 1
    
    for word in wordsPos:
        
        wordsPos[word] += smoothing_parameter
        wordsPos[word] /= ((len(wordsPos) * smoothing_parameter) + poscount)
        wordsPos[word] = math.log(wordsPos[word])

    for word in wordsNeg:
        
        wordsNeg[word] += smoothing_parameter
        wordsNeg[word] /= ((len(wordsNeg) * smoothing_parameter) + negcount)
        wordsNeg[word] = math.log(wordsNeg[word])

    for review in dev_set:
        
        posProb = 0
        negProb = 0
        
        for word in review:
            
            try:
                posProb += wordsPos[word]  
            except:
                temp = smoothing_parameter/((len(wordsPos) * smoothing_parameter) + poscount)
                posProb += math.log(temp)
            try:
                negProb += wordsNeg[word]
            except:
                temp = smoothing_parameter/((len(wordsNeg) * smoothing_parameter) + negcount)
                negProb += math.log(temp)

        posProb += math.log(pos_prior)
        negProb += math.log(1-pos_prior)

        # posProb = math.log(posProb)
        # negProb = math.log(negProb)
        # print("posProb:", posProb)
        # print("negProb:", negProb)
        # if posProb/negProb > (1-pos_prior)/pos_prior:
        if posProb > negProb:
            # print("pos")
            ret.append(1)
        else:
            # print("neg")
            ret.append(0)    
    # print(ret)
    return ret