# WHERE TO GO NEXT?
This is a destination recommendation system for place of interests and restaurants in London. The databased used to build the recommendation engine consists of around 1200 place of interest (museums, libraries, parks, landmarks) and 1500 restaurants(also including coffee shops, bakeries, bars, etc.) in London area.

## Dataset
Scraped from tripadvisor. 

## Installation
This app run as flask web app. Make sure you have python 3 installed and also install the required libraries in requirements.txt. 

```pip install -r requirements.txt```

Then run the app from terminal

```python3 routes.py```

It will start the localhost server at ```localhost:5000```, put it in your browser and you can access the app.

## How it works
You can either search for recommendation for Place of Interests or Restaurants. Put the name of your destination, and this app will recommend similar place to visit. The results are sorted by popularity and distance to your destination. Make sure you input the correct name of the place (see list of places registered on the page), otherwise it will throw error.
