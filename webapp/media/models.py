import datetime
from .. import db

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL (replace with your actual database URL)
DATABASE_URL = "sqlite:///./mydatabase.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

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

# Create the database tables
Base.metadata.create_all(engine)

# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example usage:

# Create a database session
db = SessionLocal()

try:
    # Create some actors
    actor1 = Actor(first_name="Leonardo", last_name="DiCaprio")
    actor2 = Actor(first_name="Brad", last_name="Pitt")
    actor3 = Actor(first_name="Kevin", last_name="Bacon")
    actor4 = Actor(first_name="Tom", last_name="Hanks")

    # Create some directors
    director1 = Director(first_name="Christopher", last_name="Nolan")
    director2 = Director(first_name="Ron", last_name="Howard")
    director3 = Director(first_name="Robert", last_name="Zemeckis")

    db.add_all([actor1, actor2, actor3, actor4])
    db.commit()

    # Create some movies and associate actors
    movie1 = Movie(title="Inception", director=director1 actors=[actor1, actor2])
    movie2 = Movie(title="Apollo 13", director=director2, 
                   actors=[actor3, actor4],
                   year=1995, IsMovie=True,
                   PersonalRating=10)
    movie3 = Movie(title="Forrest Gump", director=director3, actors=[actor4])
    movie4 = Movie(title="Once Upon a Time in Hollywood", director="Quentin Tarantino", actors=[actor2, actor1])

    db.add_all([movie1, movie2, movie3, movie4])
    db.commit()

    # Query movies and their actors
    print("\nMovies and their Actors:")
    movies = db.query(Movie).all()
    for movie in movies:
        actor_names = [f"{actor.first_name} {actor.last_name}" for actor in movie.actors]
        print(f"Title: {movie.title}, Director: {movie.director}, Actors: {', '.join(actor_names)}")

    # Query actors and the movies they starred in
    print("\nActors and their Movies:")
    actors = db.query(Actor).all()
    for actor in actors:
        movie_titles = [movie.title for movie in actor.movies]
        print(f"Actor: {actor.first_name} {actor.last_name}, Movies: {', '.join(movie_titles)}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database session
    db.close()

