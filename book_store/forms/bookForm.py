from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre')
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Book')
