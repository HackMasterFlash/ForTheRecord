from ..media.models import db, Actor, Movie, Director
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Define the database URL (replace with your actual database URL)
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')

# Create a SQLAlchemy engine
engine = db.create_engine(DATABASE_URL)

Base = declarative_base()

# Create the database tables
Base.metadata.create_all(engine)

# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example usage:

# Create a database session
db_local = SessionLocal()

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

    db_local.add_all([actor1, actor2, actor3, actor4])
    db_local.commit()

    # Create some movies and associate actors
    movie1 = Movie(title="Inception", director=director1, actors=[actor1, actor2])
    movie2 = Movie(title="Apollo 13", director=director2, 
                   actors=[actor3, actor4],
                   year=1995, IsMovie=True,
                   PersonalRating=10)
    movie3 = Movie(title="Forrest Gump", director=director3, actors=[actor4])
    movie4 = Movie(title="Once Upon a Time in Hollywood", director="Quentin Tarantino", actors=[actor2, actor1])

    db_local.add_all([movie1, movie2, movie3, movie4])
    db_local.commit()

    # Query movies and their actors
    print("\nMovies and their Actors:")
    movies = db_local.query(Movie).all()
    for movie in movies:
        actor_names = [f"{actor.first_name} {actor.last_name}" for actor in movie.actors]
        print(f"Title: {movie.title}, Director: {movie.director}, Actors: {', '.join(actor_names)}")

    # Query actors and the movies they starred in
    print("\nActors and their Movies:")
    actors = db_local.query(Actor).all()
    for actor in actors:
        movie_titles = [movie.title for movie in actor.movies]
        print(f"Actor: {actor.first_name} {actor.last_name}, Movies: {', '.join(movie_titles)}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database session
    db_local.close()