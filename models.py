from recommender_engine import resto_recommender,poi_recommender, get_place_name
import json

class Recommendation(object):
	def poi_query(self,destination_name):
		result = json.loads(poi_recommender(destination_name))	
		recommended = []
		for row in result:
			name = row['place_name']
			url = row['place_name_link']
			image = row['thumbnail_image']
			postcode = row['postcode']
			score = row['relative_score']
			category = row['categories']

			d = { 
			'name': name,
			'url': url,
			'image': image,
			'postcode': postcode,
			'score': score,
			'category': category
			}
			recommended.append(d)
		return recommended

	def resto_query(self,destination_name):
		result = json.loads(resto_recommender(destination_name))	
		recommended = []
		for row in result:
			name = row['name']
			url = row['name_link']
			image = row['thumbnail']
			postcode = row['postcode']
			score = row['relative_score']
			category = row['cuisines_categories']

			d = { 
			'name': name,
			'url': url,
			'image': image,
			'postcode': postcode,
			'score': score,
			'category': category
			}
			recommended.append(d)
		return recommended

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