import pandas as pd
import numpy as np

# various preprocessing

def combine_categories(categories_series):
	# put everything on lowercase
	categories = categories_series.str.lower()
	# remove separator to get category soup
	categories = categories.str.replace(",","")
	return categories

def clean_unwanted_chars(str_series):
	ignore_char = ['!','&','?',';', '.',',','”','“']
	for char in ignore_char:
		str_series = str_series.str.replace(char,"")
	return str_series

def column_processing(df):
	df.drop_duplicates(subset=['place_name'],inplace=True)
	df.drop(['url_x','review_count_x','review_count_link','thumbnail_image_alt','thumbnail_image_link'],axis=1,inplace=True)
	df.rename(index=str, columns={"review_count_y": "review_count", "thumbnail_x": "thumbnail", "cuisines_block_y":'cuisines_block'},inplace=True)
	return df

def populate_null(df):
	df['review_count'].fillna("0",inplace=True)
	df['rating'].fillna(0,inplace=True)
	df['reviews_combined'].fillna("",inplace=True)
	return df

# main
def main():	
	df = pd.read_csv('data/merged_poi.csv')
	print('cleaning & preprocessing')
	df = column_processing(df)

	#drop if more than 3 columns are null
	df.dropna(axis=0,thresh=4,inplace=True)

	df['categories_all'] = combine_categories(df.categories)
	df['reviews_combined'] = df.review_talk_1 + " "+ df.review_talk_2  + " " + df.review_talk_3 
	df['reviews_combined'] = df.reviews_combined.fillna("")
	print("\n", df['reviews_combined'].head())	
	df['reviews_combined'] = clean_unwanted_chars(df.reviews_combined)
	df = populate_null(df)
	df['postcode'] = df.postcode.astype(str).str[7:-1]
	df['rev_cat_soup'] = df.reviews_combined + " " + df.categories_all + df.place_name.str.lower()
	print("\n", df['rev_cat_soup'].head())



	df.to_csv('data/cleaned_poi.csv',index=False)
	print('file saved')

if __name__ == "__main__":
	main()