import os
import subprocess
import regex as re
import sys
import nltk
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd
import numpy as np
from smart_open import open
import time
import sys
'''def remove_spaces(sentence):	
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
		doc_nospace = doc_nospace+i
	return doc_nospace

def create_tagged_document(list_of_list_of_words,category_num):
	for list_of_words in list_of_list_of_words:
		yield gensim.models.doc2vec.TaggedDocument(list_of_words, [category_num])'''

cat_df = pd.read_excel("Category_info.xlsx",sheet_name='Sheet1')
cat_df.columns = ['Category','Count','Url']

df = pd.read_excel("Meta_data_train_and_test.xlsx",sheet_name='Sheet')
df = df.reindex(np.random.permutation(df.index))
row = 1

cat_tags = dict() 
train_data = []

for i in range(0,150):
	cat_tags[cat_df.at[i,'Category']] = i 
use_old = sys.argv[1]

if use_old != 0:
	model = Doc2Vec.load("d2v.model")
else:
	for row in range(0,80):
	
		category = df.at[row,'Category']	
		libname = df.at[row,'Name']
		path = df.at[row,'Path']
	
		doc  = open(path).read()
		train_data.append(TaggedDocument(doc.split(), [cat_tags[category]]))

	max_epochs = 100
	vec_size = 20
	alpha = 0.025
	model = Doc2Vec(vector_size=vec_size,
				alpha=alpha, 
				min_alpha=0.00025,
				min_count=1,
				dm =1)
  
	model.build_vocab(train_data)
	path = df.at[101,'Path']
	
	doc  = open(path).read()
	
	for epoch in range(max_epochs):
		print('iteration {0}'.format(epoch))
		model.train(train_data,
				total_examples=model.corpus_count,
				epochs=model.iter)
		# decrease the learning rate
		model.alpha -= 0.0002
		# fix the learning rate, no decay
		model.min_alpha = model.alpha

	model.save("d2v.model")
	print("Model Saved")