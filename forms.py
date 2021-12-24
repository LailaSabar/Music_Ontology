from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from flask_wtf import FlaskForm

class SearchForm(FlaskForm):
  search = StringField('', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-success btn-block'})

class SearchForm2(FlaskForm):
    search2 = StringField('', [DataRequired()])
    submit2 = SubmitField('Search',
                           render_kw={'class': 'btn btn-success btn-block'})
