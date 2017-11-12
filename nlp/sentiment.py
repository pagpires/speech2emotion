from gensim import models
import numpy as np
import pandas as pd
import sys
import os


def import_model():
    """
    import the model for word to vec
    it takes sometime and we only need to do it once at the start
    """
    return models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)


def emotion_score(words, model2):  
    """
    convert a list of clean word strings to scores in emotions
    it also takes the imported dictionary model2
    """
    word_txt = words.split()
    txt_wordvec = np.zeros((1,300))
    for i in range(len(word_txt)):
        word=word_txt[i].lower()
        if word in model2.vocab:
            txt_wordvec+=model2[word]  

    emotions = ['anger','contempt','disgust','fear','happiness','neutral','surprise','sadness']
    emotions_wordvec = np.zeros((len(emotions),300))
    for i in range(len(emotions)):
        emo = emotions[i]
        if emo in model2.vocab:
            emotions_wordvec[i] = model2[emo] 
            
    res = np.dot(emotions_wordvec,np.reshape(txt_wordvec,300,1)) 
    res = np.exp(res)
    score = res/np.sum(res)
    score = score.reshape((1,8))
    return (score, emotions)

def moving_average(ans_all, i):
    """
    i is the index of current chunck
    we take the average over min(i,7) chuncks
    """
    if i < 6:
        return ans_all[:i+1].mean()
    else:
        return ans_all[i-6:i+1].mean()