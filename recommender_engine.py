import pandas as pd
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# various preprocessing
def get_stemmed_words(df,col_name):
	stemmer = PorterStemmer()
	df['reviews_stemmed'] = df[col_name].astype('str')
	df['reviews_stemmed'] = df['reviews_stemmed'].apply(lambda y: stemmer.stem(y))
	return df

def combine_categories(categories_series,splitter=";"):
	# put everything on lowercase
	categories = categories_series.str.lower()
	# remove space (some categories consist of two words)
	categories = categories.str.replace(" ","")
	categories = categories.str.replace(splitter," ")
	return categories

def clean_unwanted_chars(str_series):
	ignore_char = ['!','&','?',';', '.',',','”','“']
	for char in ignore_char:
		str_series = str_series.str.replace(char,"")
	return str_series

def get_wordsoup(df,cols):
	# input cols as list of column names
	for col in cols:
		df['wordsoup'] += (" " + df[col])
	return df

def get_review_count_quintile(df):
	df.review_count.fillna(0,inplace=True)
	df['review_count'] = df.review_count.str.replace(',',"")
	q = pd.qcut(df.review_count.astype(int),5,labels=[1,2,3,4,5])
	return q

def get_place_popularity(df):
	df['rating'].fillna(0,inplace=True)
	df['count_quintile'] = get_review_count_quintile(df)
	df['popularity_index'] = df['count_quintile'] * df['rating'].astype(int)
	return df

# tf-idf & similarity
def get_tfidf(wordsoup_series):
	tfidf = TfidfVectorizer(stop_words='english')
	wordsoup_series = wordsoup_series.fillna('')
	tfidf_matrix = tfidf.fit_transform(wordsoup_series)
	return tfidf_matrix

def get_cosine_sim(tfidf_matrix):
	cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
	return cosine_sim


# aggregated
def sort_result(df_result):
	# calculate relative score between the recommended places for sorting
	# scale is 0 - 10
	df_result = get_place_popularity(df_result)
	max_popularity = df_result['popularity_index'].max()
	max_similarity = df_result['similarity_score'].max()
	# give more weight for similarity
	df_result['relative_score'] = 10* (df_result['popularity_index'].divide(max_popularity)) * (df_result['similarity_score'].divide(max_similarity))
	return df_result.sort_values('relative_score',ascending=False)

def get_recommendation(df,destination, index_col,cosine_sim):
	indices = pd.Series(df.index,index=df[index_col])
	idx = int(indices[destination])
	similarity_scores = list(enumerate(cosine_sim[idx]))
	similarity_scores = sorted(similarity_scores, key=lambda x:x[1],reverse = True)
	# only consider top 5 most similar
	similarity_scores = similarity_scores[1:6]
	rec_indices = [i[0] for i in similarity_scores]
	df_result = df.iloc[rec_indices]
	score_list = [score[1] for score in similarity_scores]
	df_result['similarity_score'] = score_list	
	# return only top 5 after sorting
	return sort_result(df_result)







	






