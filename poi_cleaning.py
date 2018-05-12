import pandas as pd
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer

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

def main():	
	df = pd.read_csv('data/merged_poi.csv')
	print('cleaning & preprocessing')
	df.drop_duplicates(subset=['place_name'],inplace=True)
	df.drop(['url_x','review_count_x','review_count_link','thumbnail_image_alt','thumbnail_image_link'],axis=1,inplace=True)
	df.rename(index=str, columns={"review_count_y": "review_count", "thumbnail_x": "thumbnail", "cuisines_block_y":'cuisines_block'},inplace=True)
	

	df['categories_all'] = combine_categories(df.categories)
	df['reviews_combined'] = df.review_talk_1 + " "+ df.review_talk_2  + " " + df.review_talk_3 
	print("\n", df['reviews_combined'].head())
	
	df['reviews_combined'] = clean_unwanted_chars(df.reviews_combined)
	
	df = get_stemmed_words(df,'reviews_combined')
	print("\n", df['reviews_stemmed'].head())
	print(df['reviews_stemmed'].head())
	df['rev_cat_soup'] = df.reviews_stemmed + " " + df.categories_all
	print("\n", df['rev_cat_soup'].head())
	df.to_csv('data/cleaned_poi.csv',index=False)
	print('file saved')
main()