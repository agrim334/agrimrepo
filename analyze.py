import regex as re
import sys
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd
import numpy as np
from smart_open import smart_open
from smart_open import open
import time
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import multiprocessing

def read_corpus(fname,label,tokens_only=False):
	with open(fname) as f:
		f_temp = f.read().split('}')
		for line in f_temp:
			if tokens_only:
				yield gensim.utils.simple_preprocess(line)
			else:
				# For training data, add tags
				yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [label])
def heatconmat(y_true,y_pred):
	sns.set_context('talk')
	plt.figure(figsize=(9,6))
	sns.heatmap(confusion_matrix(y_true,y_pred))
	plt.show()
	print(classification_report(y_true,y_pred))

cat_df = pd.read_excel("Category_info.xlsx",sheet_name='Sheet1')
cat_df.columns = ['Category','Count','Url']

df = pd.read_excel("Meta_data_train_and_test.xlsx",sheet_name='Sheet')
df.columns = ['Name','License','Category','Tags','Count','Path']
df = df.reindex(np.random.permutation(df.index))

train, test = train_test_split(df[:150], test_size=0.3)
del df
cat_tags = dict() 
train_data = list()
test_data = list()
y_train = []
y_test = []
cores = multiprocessing.cpu_count()

for i in range(0,150):
	cat_tags[cat_df.at[i,'Category']] = i 

for row in range(0,train.shape[0]):
	category = train.loc[train.index[row],'Category']	
	libname = train.loc[train.index[row],'Name']
	path = train.loc[train.index[row],'Path']
	y_train.append(category)
	with open(path) as f:
		f_temp = f.read().split('}')
		for line in f_temp:
			train_data.append(TaggedDocument(line, [cat_tags[category]]))

for row in range(0,test.shape[0]):
	
	category = test.loc[test.index[row],'Category']	
	libname = test.loc[test.index[row],'Name']
	path = test.loc[test.index[row],'Path']
	y_test.append(category)
	with open(path) as f:
		f_temp = f.read().split('}')
		for line in f_temp:
			test_data.append(TaggedDocument(line, [cat_tags[category]]))

print("data done")
max_epochs = 10
vec_size = 80
alpha = 0.5
model = Doc2Vec(vector_size=vec_size,
				alpha=alpha, 
				min_alpha=0.00025,
				dm =1,workers=cores)
model.build_vocab(train_data)

model.train(train_data,
			total_examples = model.corpus_count,
			epochs = max_epochs)
print("trained")
X_train = np.array([model.docvecs[i[1][0]] for i in train_data])
y_train = np.array([i[1][0] for i in train_data])
y_test = np.array([i[1][0] for i in test_data])
X_test = np.array([model.infer_vector(test_data[i][0].split('}')) for i in range(len(test_data))])

print("Feature set")
lrc = LogisticRegression(multi_class='multinomial', solver='lbfgs',max_iter=1000000,n_jobs = -1)
Gaussian_clf = svm.SVC(kernel = 'rbf')
linear_clf = svm.SVC(kernel = 'linear')

'''lrc.fit(X_train,y_train)
y_pred = lrc.predict(X_test)
heatconmat(y_test,y_pred)
'''
Gaussian_clf.fit(X_train,y_train)
y_pred = Gaussian_clf.predict(X_test)
heatconmat(y_test,y_pred)
'''
linear_clf.fit(X_train,y_train)
y_pred = linear_clf.predict(X_test)
heatconmat(y_test,y_pred)
'''