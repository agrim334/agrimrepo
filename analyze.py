import os
import subprocess
import regex as re
import sys
import nltk
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedLineDocument
import pandas as pd
import numpy as np

def remove_spaces(sentence):	
	sent = ""
	k = sentence.split('\n')
	for i in k:
		sent = sent+i
	sent = re.sub(r'\s+','  ',sent)
	return sent

def tokenizer(path):
	file = open(path).read()
	doc = file.split('}')
	doc_nospace = ""
	for i in doc:
		i = i + '}'
		i = remove_spaces(i)
		doc_nospace = doc_nospace+(i)
	return doc_nospace

df = pd.read_excel("Meta_data_train_and_test.xlsx",sheet_name='Sheet')
df = df.reindex(np.random.permutation(df.index))
row = 1
corpus = list()
for row in range(0,548):
	
	category = df.at[row,'Category']
	
	libname = df.at[row,'Name']

	path = df.at[row,'Path']
	doc = tokenizer(path)
	corpus.append((doc.split(),category))

paras=TaggedDocument(corpus)
print(paras)

max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(iter(paras))

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")