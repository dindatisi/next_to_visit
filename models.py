from recommender_engine import resto_recommender,poi_recommender, get_place_name

class Recommendation(object):
	def query(self,destination_name):
		return poi_recommender(destination_name)

	def get_name(self,recommendation):
		names = recommendation.place_name.values.tolist()
		print(names)
		return names

class Places(object):
	def get_poi(self):
		places = get_place_name('poi')
		return places

	def get_resto(self):
		places = get_place_name('resto')
		return places