import pandas as pd
import recommender_engine as re

def main():	
	df = pd.read_csv('data/cleaned_poi.csv')
	cosine_sim = re.get_count_similarity(df, df.rev_cat_soup.astype(str))
	df_result = re.get_recommendation(df,'Camden Arts Center', 'place_name',cosine_sim)
	print(df_result[['place_name','relative_score','similarity_score','popularity_index','categories','reviews_combined']])
main()
