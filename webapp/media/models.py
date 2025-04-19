import datetime
from .. import db

# Define the association table for the many-to-many relationship between Movie and Actor
movie_actor_association = db.Table(
    'movie_actor', db.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

# Define the Movie model
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True, nullable=False)
    director = db.relationship("Director", back_populates="movies")
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    actors = db.relationship("Actor", secondary=movie_actor_association, back_populates="movies")
    year = db.Column(db.Integer)
    IsMovie = db.Column(db.Boolean)
    # EpisodeTitle = db.Column(db.String(96))
    Season = db.Column(db.Integer)
    Episode = db.Column(db.Integer)
    Source = db.Column(db.String(96))
    DateViewed = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    PersonalRating = db.Column(db.Integer)
    RatingSource = db.Column(db.String(96))
    RatingValue = db.Column(db.Float)
    RatingValueString = db.Column(db.String(96))
    PosterURL = db.Column(db.String(255))
    PosterLocalURL = db.Column(db.String(255))
    plot = db.Column(db.String(512))

    def __repr__(self):
        return f"<Movie(title='{self.title}', director='{self.director}', id='{self.id}')>"
    
    def actors_to_string(self):
        result = ""
        for i, actor in enumerate(self.actors):
            if i == 0:
                result = "{0} {1}".format(actor.first_name,actor.last_name)
            else:
                result = "{0}, {1} {2}".format(result, actor.first_name, actor.last_name)
        return result
    
    def omdb_factory(self, omdb_data):
        """
        Populate the movie object fields with data from the OMDB API response.

        Args:
            omdb_data (dict): The OMDB API response data.
        """
        self.title = omdb_data.get('Title')
        director_name = omdb_data.get('Director')
        if director_name:
            director_name = director_name.split(' ')
            if len(director_name) > 1:
                self.director = Director(first_name=' '.join(director_name[:-1]), last_name=director_name[-1])           
            else:
                self.director = Director(last_name=director_name[0])
        else:
            self.director = None        
        actors_str = omdb_data.get('Actors')
        actors_array = []
        for each_actor in actors_str.split(','):
            an_actor = Actor()
            an_actor.define_from_actor_fullname(each_actor)
            actors_array.append(an_actor)
        self.actors = actors_array
        self.year = omdb_data.get('Year')
        self.IsMovie = (omdb_data.get('Type') == 'movie')
        self.plot = omdb_data.get('Plot')
        self.PosterUrl = omdb_data.get('Poster')
        the_ratings = omdb_data.get('Ratings')
        self.RatingSource = None
        # Check to see if there is a Rotten Tomatoes rating in the list of ratings
        # If there is, set the rating_source and rating fields accordingly
        # If there is no Rotten Tomatoes rating, check for an Internet Movie Database rating
        if the_ratings:
            for rating in the_ratings:
                if rating.get('Source') == 'Rotten Tomatoes':
                    self.RatingSource = 'Rotten Tomatoes'
                    self.RatingValueString = rating.get('Value')
                    break
            if self.RatingSource is None:
                for rating in the_ratings:
                    if rating.get('Source') == 'Internet Movie Database':
                        self.RatingSource = 'Internet Movie Database'
                        self.RatingValueString = rating.get('Value')
                        break
        else:
            self.RatingSource = None
            self.RatingValueString = None

    # def actor_factory_from_actor_fullname(self, actor_fullname):
    #     actor_name = actor_fullname.split(' ')
    #     if len(actor_name) > 2:
    #         actor_name = Actor(first_name=' '.join(actor_name[:-1]), last_name=actor_name[-1])
    #     elif len(actor_name) == 2:
    #         actor_name = Actor(first_name=actor_name[0], last_name=actor_name[1])
    #     else:
    #         an_actor = Actor( last_name=actor_fullname)
    #     return an_actor
    

# Define the Actor model
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    def define_from_actor_fullname(self, actor_fullname):
        actor_name = actor_fullname.split(' ')
        if len(actor_name) > 2:
            self.first_name=' '.join(actor_name[:-1])
            self.last_name=actor_name[-1]
        elif len(actor_name) == 2:
            self.first_name=actor_name[0]
            self.last_name=actor_name[1]
        else:
            self.last_name=actor_fullname
        
    
# Define the Director model
class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", back_populates="director")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
