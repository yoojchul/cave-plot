import matplotlib.pyplot as plt
import urllib.request
import numpy as np
from math import log10, floor 

prev_rate = "."
prev_gold = "."
with urllib.request.urlopen("https://drive.google.com/uc?export=down&id=13BYaGCdjvb91pRu_GGkydpCf_O95eND3") as f:
    f.readline() # header
    data = []
    for s in f:
        ymd, rate, gold = s.decode('utf-8').rstrip().split(' ')
        if rate == ".":   #  . means null and copies from the previous
            rate = prev_rate
        if gold == ".":
            gold = prev_gold
        data.append([ymd, float(rate), float(gold)])
        prev_rate = rate
        prev_gold = gold

max_rate = 0   # find max of rate
max_gold = 0  # find max of gold
for y in data:
    _, rate, gold = y
    if max_rate < rate:
        max_rate = rate
    if max_gold < gold:
        max_gold = gold
        
fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.set_ylabel('DGS10', color='b')
ax1.tick_params('y', colors='b')

rates = []
golds = []
ind = []
year_labels = []
i = 1
s_year = "2009"
for y in data:
    ymd, r, g = y
    rates.append(float(r)/max_rate)   # normalize 
    golds.append(1.0-float(g)/max_gold + 0.8)  # normalize and inverse, plus again
    if s_year != ymd[0:4]:
        ind.append(i)
        s_year = ymd[0:4]
        year_labels.append(s_year)
    i += 1
ax1.set_xticks(ind)   #  Jan 1, or 2 or 3
ax1.set_xticklabels(year_lables)  #  years for labels 
    
ax1.plot(rates, color='b')
ax1.plot(golds, color='r')

ax1.set_yticks(np.arange(0.2, 1.4, 0.2))  # six ticks from 0.2 to 1.2 
ytick_labels = []
for i in np.arange(0.2, 1.4, 0.2):
    v = i * max_rate   # normalized to real 
    w = round(v,  1-int(floor(log10(abs(v)))))  # two digits are valid 
    ytick_labels.append(str(w))
ax1.set_yticklabels(ytick_labels)

y1, y2 = ax1.get_ylim()

ax2 = ax1.twinx()  #  share x, different y axis
ax2.set_ylabel('Gold', color='r')
ax2.tick_params('y', colors='r')
ax2.set_ylim(y1, y2)
ax2.set_yticks(np.arange(0.2, 1.4, 0.2))

ytick_labels = []
for i in np.arange(0.2, 1.4, 0.2):   # six ticks from 0.2 to 1.2 
    v = (1.0 + 0.8 - i) * max_gold  # normalized to real 
    w = round(v,  1-int(floor(log10(abs(v)))))  # two digits are valid 
    ytick_labels.append(str(w))
ax2.set_yticklabels(ytick_labels)

fig.tight_layout()
plt.show()