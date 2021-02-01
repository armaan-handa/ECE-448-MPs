"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np
import time
import math
def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    predicts = []
    tags = {}
    wordtags = {}
    for sentence in train:
        for wordtag in sentence:
            try:
                wordtags[wordtag] += 1
            except:
                wordtags[wordtag] = 1
            try:       
                tags[wordtag[1]] += 1
            except:
                tags[wordtag[1]] = 1
    
    for sentence in test:
        predicts.append([])
        for word in sentence:
            predicttag = (tags.keys(), 0)
            for tag in tags:
                if (word, tag) in wordtags:
                    if wordtags[(word, tag)] > predicttag[1]:
                        predicttag = (tag, wordtags[(word, tag)])
            if predicttag[1] == 0:
                for tag in tags:
                    if tags[tag] > predicttag[1]:
                        predicttag = (tag, tags[tag])
            predicts[-1].append((word, predicttag[0]))
    return predicts


def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    starttime = time.time()
    transitions = {}
    emissions = {}
    initials = {}
    tagcount = {}
    vocab = {}
    initialscount = 0
    transitionscount = 0
    emissioncount = 0
    k = 0.00001
    for sentence in train:
        for i in range(len(sentence)):
            tag = sentence[i][1]
            word = sentence[i][0]
            if word not in vocab:
                vocab[word] = 1
            try:
                tagcount[tag] += 1
            except:
                tagcount[tag] = 1
            if i == 0:
                try:
                    initials[tag] += 1
                except:
                    initials[tag] = 1
                initialscount += 1
            try:
                emissions[(word, tag)] += 1
            except:
                emissions[(word, tag)] = 1
            emissioncount += 1
            if i < len(sentence) - 1:
                next_tag = sentence[i+1][1]
                try:
                    transitions[(tag, next_tag)] += 1
                except:
                    transitions[(tag, next_tag)] = 1
                transitionscount += 1
    # initialstotal = 0
    for tag in initials:
        initials[tag] += k
        initials[tag] /= initialscount + k*(len(tagcount)+1)
        # initialstotal+= initials[tag]
        # print(tag, initials[tag])
        initials[tag] = (math.log(initials[tag]))
        # print(tag, initials[tag])
    # print(initialstotal)
    # transitiontotal = 0
    for tagpair in transitions:
        transitions[tagpair] += k
        transitions[tagpair] /= transitionscount + k*(len(tagcount))
        # transitiontotal += transitions[tagpair]
        # print(tagpair, transitions[tagpair])
        transitions[tagpair] = (math.log(transitions[tagpair]))
        # print(tagpair, transitions[tagpair])
    # print(transitiontotal)
    for emission in emissions:
        emissions[emission] += k
        emissions[emission] /= tagcount[emission[1]] + k*(len(vocab) + 1)
        emissions[emission] = (math.log(emissions[emission]))
        # print(emission, emissions[emission])

    viterbi_matrix = []
    predicts = []
    prevword = 'init'
    for sentence in test:
        viterbi_matrix.append({})
        j = 0
        for word in sentence:
            viterbi_matrix[-1][word] = {}
            if j == 0:
                for tag in initials:
                    viterbi_matrix[-1][word][tag] = (float('-inf'), 'init')
                    try:
                        emissionprob = emissions[(word, tag)]
                    except:
                        emissionprob = (math.log(k/(tagcount[tag] + k*(len(vocab)+1))))
                    try:
                        initprob = initials[tag]
                    except:
                        initprob = (math.log(k/(initialscount) + k*(len(tagcount)+1)))
                    if (initprob + emissionprob) > viterbi_matrix[-1][word][tag][0]:
                        viterbi_matrix[-1][word][tag] = (initprob + emissionprob, 'init')
                        # print((initials[tag] + emissionprob, 'init'))
            else:
                for prev_tag in tagcount:
                    for tag in tagcount:
                        tagpair = (prev_tag, tag)
                        if tag not in viterbi_matrix[-1][word]:
                            viterbi_matrix[-1][word][tag] = (float('-inf'), prev_tag)
                        try:
                            transitionprob = transitions[tagpair]
                        except:
                            transitionprob = (math.log(k/(transitionscount + k*len(tagcount))))
                        try:
                            emissionprob = emissions[(word, tag)]
                        except:
                            emissionprob = (math.log(k/(tagcount[tag] + k*(len(vocab)+1))))
                        if (transitionprob + emissionprob + viterbi_matrix[-1][prevword][prev_tag][0] > viterbi_matrix[-1][word][tag][0]):
                            viterbi_matrix[-1][word][tag] = (transitionprob + emissionprob + viterbi_matrix[-1][prevword][prev_tag][0], prev_tag)
                            # print(tag)
                            # print(viterbi_matrix[-1][word][tag])
                            # print('------------')
            
            prevword = word
            j += 1
    i = 0
    # print(viterbi_matrix[-1])
    for sentence in test:
        predicts.append([])
        tagmax = (max(tagcount), float('-inf'))
        # print(tagmax)
        for tag in tagcount:
            if viterbi_matrix[i][sentence[-1]][tag][0] > tagmax[1]:
                # print(tagmax)
                tagmax = (tag, viterbi_matrix[i][sentence[-1]][tag][0])
                # print(tagmax)
                # print('-----------')
        predicts[-1].insert(0, (sentence[-1],tagmax[0]))
        for j in range(len(sentence) - 1):
            predicts[-1].insert(0,(sentence[-(j+2)], viterbi_matrix[i][sentence[-(j+1)]][tagmax[0]][1]))
            # print(tagmax)
            tagmax = (viterbi_matrix[i][sentence[-(j+1)]][tagmax[0]][1], 0)
        # print('----------')
        i += 1
    endtime = time.time()
    elapsed = endtime-starttime
    print(elapsed)
    return predicts

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''


    predicts = []
    raise Exception("You must implement me")
    return predicts