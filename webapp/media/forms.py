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
    actors = StringField('Cast', [Length(max=255)])
    year = IntegerField('Year')
    plot = TextAreaField('Plot', [Length(max=512)])
    poster_url = StringField('Poster URL', [Length(max=255)])
    rating_source = StringField('Rating Source', [Length(max=128)])
    rating = StringField('Rating', [Length(max=128)])

    def omdb_factory(self, omdb_data):
        """
        Populate the form fields with data from the OMDB API response.

        Args:
            omdb_data (dict): The OMDB API response data.
        """
        self.title.data = omdb_data.get('Title')
        self.director.data = omdb_data.get('Director')
        self.actors.data = omdb_data.get('Actors')
        self.year.data = omdb_data.get('Year')
        self.plot.data = omdb_data.get('Plot')
        self.poster_url.data = omdb_data.get('Poster')
        the_ratings = omdb_data.get('Ratings')
        self.rating_source.data = None
        # Check to see if there is a Rotten Tomatoes rating in the list of ratings
        # If there is, set the rating_source and rating fields accordingly
        # If there is no Rotten Tomatoes rating, check for an Internet Movie Database rating
        if the_ratings:
            for rating in the_ratings:
                if rating.get('Source') == 'Rotten Tomatoes':
                    self.rating_source.data = 'Rotten Tomatoes'
                    self.rating.data = rating.get('Value')
                    break
            if self.rating_source.data is None:
                for rating in the_ratings:
                    if rating.get('Source') == 'Internet Movie Database':
                        self.rating_source.data = 'Internet Movie Database'
                        self.rating.data = rating.get('Value')
                        break
        else:
            self.rating_source.data = None
            self.rating.data = None
        
