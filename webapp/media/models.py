import datetime
from .. import db

# from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define a base for declarative models
Base = declarative_base()

# Define the association table for the many-to-many relationship between Movie and Actor
movie_actor_association = db.Table(
    'movie_actor', Base.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)
# between movie and director
movie_director_association = db.Table(
    'movie_director', Base.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('directors.id'), primary_key=True)
)

# Define the Movie model
class Movie(Base):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True)
    director = relationship("Director", secondary=movie_director_association, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actor_association, back_populates="movies")
    year = db.Column(db.Integer)
    IsMovie = db.Column(db.Boolean)
    # EpisodeTitle = db.Column(db.String(96))
    Season = db.Column(db.Integer)
    Episode = db.Column(db.Integer)
    Source = db.Column(db.String(96))
    DateViewed = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    PersonalRating = db.Column(db.Integer)
    RatingSource = db.Column(db.String(96))
    RatingValue = db.Column(db.float)

    def __repr__(self):
        return f"<Movie(title='{self.title}', director='{self.director}')>"
    

# Define the Actor model
class Actor(Base):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    movies = relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __repr__(self):
        return f"<Actor('{self.first_name}' '{self.last_name}')>"
    
# Define the Director model
class Director(Base):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    movies = relationship("Movie", secondary=movie_director_association, back_populates="directors")

    def __repr__(self):
        return f"<Director(f'{self.first_name}' '{self.last_name}')>"


