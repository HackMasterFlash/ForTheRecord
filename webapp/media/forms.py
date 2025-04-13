from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length


class CommentForm(Form):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

class PostForm(Form):
    title = StringField('Title', [
        DataRequired(),
        Length(max=255)
    ])
    text = TextAreaField('Content', [DataRequired()])

class MovieForm(Form):
    title = StringField('Title', [
        DataRequired(),
        Length(max=255)
        ])
    director = StringField('Director')
    actors = StringField('Cast')
    year = IntegerField('Year')
