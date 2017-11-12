# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 16:29:31 2017

@author: Xinyu Hong, Xin Liang, Yuan Liu
"""

import numpy as np

###### --------- load preprocessed arrays --------- ######

def moving_average(ans_all, i):
    """
    i is the index of current chunck
    we take the average over min(i,7) chuncks
    """
    if i < 6:
        return ans_all[:i+1].mean(0)
    else:
        return ans_all[i-6:i+1].mean(0)
scores = []
with open('scores.txt', 'r') as F:
    lines = F.readlines()
    for line in lines:
        scores.append(np.fromstring(line.rstrip(), sep=','))
scores = np.array(scores)
avg_scores = []
for i in xrange(len(scores)-1):
    avg_scores.append(moving_average(scores, i))


###### --------- load and play audio --------- ######
#from playsound import playsound
#playsound('speed.wav')

###### --------- array 2 plot 2 animation --------- ######


if __name__ == '__main__':
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
    
    def animate(i):
        global prevY, j    
        if i % 100 == 0 :
            #process real update
            y = avg_scores[j]
            j += 1
            prevY = y
        else:
            #add noise 
            sign = 1 if np.random.random() > 0.5 else -1
            y = prevY + sign * np.random.random() * 0.01
            prevY = y
        return plt.bar(x,y, tick_label=categories, color='b')
    
    anim=animation.FuncAnimation(fig,animate,blit=True, frames=n_frames, interval = 105)
    plt.show()
    
