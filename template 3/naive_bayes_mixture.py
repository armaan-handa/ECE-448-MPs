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
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
 


    # TODO: Write your code here
    wordsPos = {}
    wordsNeg = {}
    bigramPos = {}
    bigramNeg = {}
    ret = []
    posWordCount = 0
    negWordCount = 0
    posBigramCount = 0
    negBigramCount = 0
    # numOfBigrams = [0,0]
    # vocabSize = [0,0]
    labelIdx = 0

    for review in train_set:
        for i in range(len(review)):
            word = review[i]
        
            if train_labels[labelIdx] == 1:

                try:
                     wordsPos[word] += 1
                except:
                    wordsPos[word] = 1
                    # vocabSize[1] += 1

               
                posWordCount += 1

            if train_labels[labelIdx] == 0:

                try:
                    wordsNeg[word] += 1
                except:
                    wordsNeg[word] = 1
                    # vocabSize[0] += 1

                
                negWordCount += 1

            if(i+1 < len(review)):
                
                bigram = (word, review[i+1])
        
                if train_labels[labelIdx] == 1:
                    
                    try:
                        bigramPos[bigram] += 1

                    except:
                        bigramPos[bigram] = 1
                        # numOfBigrams[1] += 1

                    
                    posBigramCount += 1

                if train_labels[labelIdx] == 0:

                    try:
                        bigramNeg[bigram] += 1

                    except:
                        bigramNeg[bigram] = 1
                        # numOfBigrams[0] += 1

                    negBigramCount += 1

        labelIdx += 1

    for word in wordsPos:
        
        wordsPos[word] += unigram_smoothing_parameter
        wordsPos[word] /= ((len(wordsPos) * unigram_smoothing_parameter) + posWordCount)
        wordsPos[word] = math.log(wordsPos[word])

    for word in wordsNeg:
        
        wordsNeg[word] += unigram_smoothing_parameter
        wordsNeg[word] /= ((len(wordsNeg) * unigram_smoothing_parameter) + negWordCount)
        wordsNeg[word] = math.log(wordsNeg[word])

    for bigram in bigramPos:
        
        bigramPos[bigram] += bigram_smoothing_parameter
        bigramPos[bigram] /= ((len(bigramPos) * bigram_smoothing_parameter) + posBigramCount)
        bigramPos[bigram] = math.log(bigramPos[bigram])

    for bigram in bigramNeg:
        
        bigramNeg[bigram] += bigram_smoothing_parameter
        bigramNeg[bigram] /= ((len(bigramNeg) * bigram_smoothing_parameter) + negBigramCount)
        bigramNeg[bigram] = math.log(bigramNeg[bigram])


    for review in dev_set:
        
        posProb = 0
        negProb = 0
        posBiProb = 0
        negBiProb = 0

        for word in review:
            
            try:
                posProb += wordsPos[word]  
            except:
                temp = unigram_smoothing_parameter/((len(wordsPos) * unigram_smoothing_parameter) + posWordCount)
                posProb += math.log(temp)
            try:
                negProb += wordsNeg[word]
            except:
                temp = unigram_smoothing_parameter/((len(wordsNeg) * unigram_smoothing_parameter) + negWordCount)
                negProb += math.log(temp)
        
        posProb += math.log(pos_prior)
        posProb *= (1 - bigram_lambda)
        negProb += math.log(1-pos_prior)
        negProb *= (1 - bigram_lambda)

        for i in range(len(review) - 1):
            bigram = (review[i], review[i+1])
            try:
                negBiProb += bigramNeg[bigram]
            except:
                temp = bigram_smoothing_parameter/((len(bigramNeg) * bigram_smoothing_parameter) + negBigramCount)
                negBiProb += math.log(temp)
            try:
                posBiProb += bigramPos[bigram]
            except:
                temp = bigram_smoothing_parameter/((len(bigramPos) * bigram_smoothing_parameter) + posBigramCount)
                posBiProb += math.log(temp)

        posBiProb += math.log(pos_prior)
        negBiProb += math.log(1-pos_prior)

        posProb += (posBiProb * (bigram_lambda))
        negProb += (negBiProb * (bigram_lambda))

        if posProb > negProb:
            # print("pos")
            ret.append(1)
        else:
            # print("neg")
            ret.append(0)  

    # print(ret)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return ret