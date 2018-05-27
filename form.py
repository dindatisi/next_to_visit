from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class InputForm(Form):
	place_name = StringField('Your Destination', validators=[DataRequired("Please insert place name")])
	submit = SubmitField('Get Recommendation')