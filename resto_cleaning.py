import pandas as pd
import numpy as np


# various preprocessing
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
	df = pd.read_csv('data/merged_resto.csv')
	print('cleaning & preprocessing')
	df.drop(['url_x','review_count_x','reviews_link','thumbnail_y'],axis=1,inplace=True)
	df.rename(index=str, columns={"review_count_y": "review_count", "thumbnail_x": "thumbnail", "cuisines_block_y":'cuisines_block'},inplace=True)
	
	df['categories'] = combine_categories(df.cuisines_categories)
	df['reviews_combined'] = df.reviews + " "+df.review_talk_1 + " "+ df.review_talk_2  + " " + df.review_talk_3 
	print("\n", df['reviews_combined'].head())
	
	df['reviews_combined'] = clean_unwanted_chars(df.reviews_combined)

	df['rev_cat_soup'] = df.reviews_combined + " " + df.categories
	print("\n", df['rev_cat_soup'].head())
	df.to_csv('data/cleaned_resto.csv',index=False)
	print('file saved')
main()