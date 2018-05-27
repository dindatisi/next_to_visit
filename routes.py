from flask import Flask, render_template, request
from form import InputForm
from models import Recommendation,Places


app = Flask(__name__)

app.secret_key = "dev"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route('/restaurant', methods=['GET','POST'])
def resto_destination():
	form = InputForm()
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('restaurant.html',form=form)
		else:
			return "Success!"
	elif request.method =='GET':
		return render_template("restaurant.html", form=form)

@app.route('/place_list')
def show_places():
	place = Places()
	resto = place.get_resto()
	poi = place.get_poi()
	return render_template('place_list.html', poi=poi, resto=resto)

@app.route('/poi', methods=['GET','POST'])
def poi_destination():
	form = InputForm()

	results = []
	destination = None
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('poi.html', form=form)
		else:
			r = Recommendation()
			destination = form.place_name.data
			results = r.query(destination)
			names = r.get_name(results)
			return render_template('poi.html', form=form,destination=destination,results = names)

	elif request.method =='GET':
		return render_template("poi.html", form=form)



if __name__ == "__main__":
  app.run(debug=True)