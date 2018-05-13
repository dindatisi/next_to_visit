import pandas as pd
import recommender_engine as re

def main():	
	df = pd.read_csv('data/cleaned_resto.csv')
	print('\n calculate tfidf')
	tfidf_matrix = re.get_tfidf(df.rev_cat_soup.astype(str))
	print('matrix shape: ', tfidf_matrix.shape)
	cosine_sim = re.get_cosine_sim(tfidf_matrix)
	df_result = re.get_recommendation(df,'Flat Iron Denmark Street', 'name',cosine_sim)
	print(df_result[['name','relative_score','similarity_score','popularity_index','cuisines_categories','reviews']])
main()
