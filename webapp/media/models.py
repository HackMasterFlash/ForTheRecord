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
    

# Define the Actor model
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __repr__(self):
        return f"<Actor('{self.first_name}' '{self.last_name}')>"
    
# Define the Director model
class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", back_populates="director")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
