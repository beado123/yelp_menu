import nltk
import os
import gensim
import pickle
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

fname10 = 'mixed.model'


model10 = gensim.models.Word2Vec.load(fname10)



word = ['beef','carb','chicken','pork','cabbage','broccoli','bread','chocolate','beans','grilled','natilla']
score=0.0

for w in word:
    score += model10.similar_by_word(w, topn=3)[0][1]
    print("cbow10: ", w, model10.similar_by_word(w, topn=3))
print(score/10.0)

