
from dataclasses import replace
import os
import json
import nltk
import csv
import numpy
#from nltk.book import *
from nltk import ne_chunk, pos_tag,  word_tokenize

text0='Experience with gemtuzumab ozogamycin ("mylotarg") and all-trans retinoic acid in untreated acute promyelocytic leukemia.'
lines=nltk.word_tokenize(text0)
print(text0)
print(lines)
starts = []  # 每个tokenstr起始段在句子中的位置
ii = 0
for i in range(0,len(lines)):
    while ii < len(text0):
        if(lines[i]=='``' or lines[i]=="''"):
            lenn=1
            lines[i]='"'
        
        if text0[ii:ii + len(lines[i])]== lines[i]:
                starts.append(ii)
                print(lines[i])
                ii += len(lines[i])
                    
                break
        else:
            ii += 1
print(starts)
    