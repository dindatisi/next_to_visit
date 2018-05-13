import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

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

def get_stemmed_words(word_tokens_se):
	stemmer = SnowballStemmer('english')
	wordlist = word_tokens_se.tolist()
	stemmed = [[stemmer.stem(w) for w in i] for i in wordlist]
	return stemmed

# tf-idf & similarity
def tokenize(wordsoup_se):
	tokens = wordsoup_se.apply(lambda y: nltk.word_tokenize(y))
	stemmed_tokens = get_stemmed_words(tokens)
	return stemmed_tokens

def get_tfidf(wordsoup_series):
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	wordsoup_series = wordsoup_series.fillna('')
	tfidf_matrix = tfidf.fit_transform(wordsoup_series)
	return tfidf_matrix

def get_cosine_sim(tfidf_matrix):
	cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
	return cosine_sim

def get_count_similarity(df,col_se):
	# fill missing value with empty string
	col_se = col_se.fillna('') 
	count = CountVectorizer(tokenizer=tokenize,stop_words='english')
	count_matrix = count.fit_transform(col_se)
	# compute cosine sim
	cosine_sim = cosine_similarity(count_matrix, count_matrix)
	return cosine_sim

# aggregate for recommendation
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







	






