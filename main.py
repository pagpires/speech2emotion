# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 16:29:31 2017

@author: Xinyu Hong, Xin Liang, Yuan Liu
"""

from pydub import AudioSegment
from pydub.utils import make_chunks
import requests
import time

if __name__ == '__main__':
    ###### --------- speech 2 text --------- ######
    def chunk_speech(filename, seconds):
        myaudio = AudioSegment.from_file(filename, "wav") 
        chunks = make_chunks(myaudio, seconds * 1000)
        return chunks

    chunks = chunk_speech(r'trump_clip_demo.wav', 15)

    def speech2text(chunk):
        sub_key = r''  #REMOVE
        api_url = r'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-US&format=simple'
        headers = {
                'Ocp-Apim-Subscription-Key':sub_key,
                'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000'
                }
        content = chunk.raw_data
        res = requests.post(api_url, data=content, headers=headers)
        try:
            return res.json()['DisplayText']
        except:
            return ''

###### --------- text 2 emotion array --------- ######

    from gensim import models
    from nlp import cleanText, sentiment

    model = sentiment.import_model()

    # cleaned_text = cleanText.cleanText(s)
    # score, categories = sentiment.emotion_score(cleaned_text, model)


###### --------- array 2 plot 2 animation --------- ######
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import animation

    fig, ax=plt.subplots()
    plt.ylim(0,1)

    n_frames = 100 #Number of frames
    categories = ['anger','contempt','disgust','fear','happiness','neutral','surprise','sadness']
    n_category = len(categories)
    x = xrange(n_category)
    prevY = np.zeros(n_category)
    j = 0

    def yield_data(chunk):
        raw_text = speech2text(chunk)
        cleaned_text = cleanText.cleanText(raw_text)
        score, _ = sentiment.emotion_score(cleaned_text, model)
        return score

    def animate(i):
        global prevY, j    
    #    if i % 10 == 0 :
    #        #process real update
    #        y = yield_data(chunks[j])
    #        y = y[0]
    #        j += 1
    #        prevY = y
    #    else:
    #        #add noise 
    #        sign = 1 if np.random.random() > 0.5 else -1
    #        y = prevY + sign * np.random.random() * 0.01
    #        prevY = y
    #    
        y = yield_data(chunks[j])[0]
        j += 1
        return plt.bar(x,y, tick_label=categories, color='b')
        

    anim=animation.FuncAnimation(fig,animate,blit=True, frames=n_frames, interval = 1000)
    plt.show()

