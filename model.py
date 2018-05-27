from recommender_engine import resto_recommender,poi_recommender

class Recommendation(object):
	def query(self,destination_name):
		return poi_recommender(destination_name)

	def get_name(self,recommendation):
		names = recommendation.place_name.values.tolist()
		print(names)
		return names