import sys
import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from omdb_test_call import get_movie_data

# Assuming your module 'my_module.py' is in a directory called 'external_modules'
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if module_path not in sys.path:
    sys.path.insert(0, module_path)  # Add to the beginning for priority

from webapp.media.models import db, Actor, Movie, Director, Writer

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Define the database URL (replace with your actual database URL)
DATABASE_URL = 'sqlite:///' + os.path.join(basedir,'..', 'instance', 'mydatabase.db')
print('Trying to connect to database {0}'.format(DATABASE_URL))

# Create a SQLAlchemy engine
engine = db.create_engine(DATABASE_URL)

# # Define a base for declarative models
# class Base(DeclarativeBase):
#     pass

# the_base = Base()

# Create the database tables
# Only do this if the tables don't already exist
# Gonna ask Gemini how to do that
inspector = inspect(engine)
noActors = not inspector.has_table('actors')
noMovies = not inspector.has_table('movies')
noDirectors = not inspector.has_table('directors')
noWriters = not inspector.has_table('writers')
if ( noActors or noMovies or noDirectors or noWriters):
    db.metadata.create_all(engine)
    print('Creating table definitions')
else:
    print('Tables exist')

# Create a SessionLocal class to create database sessions
session = db.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example usage:

# Create a database session
db_local = session()

# Ask for OMDB data
title = "The Pink Panther"
omdb_data = get_movie_data(title)
if omdb_data:
    if omdb_data.get("Response") == "True":
        print("Movie data for '{0}':".format(title))
        for key, value in omdb_data.items():
            print(f"{key}: {value}")
    else:
        print(f"Error: {omdb_data.get('Error')}")

# test the Movie omdb data factory
movie1 = Movie()
movie1.omdb_factory(omdb_data)


inTable = db_local.query(Movie).filter(
        Movie.title == movie1.title).first()
if inTable:
        print('Found movie {0} in table'.format(movie1.title))
else:
    print('Did not find movie {0} in table. Need to add.'.format(movie1.title))
    db_local.add(movie1)
    something_to_commit = True

    if something_to_commit:
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

# Query writers and the movies they wrote for
print("\nWriters and their Movies:")
writers = db_local.query(Writer).all()
for writer in writers:
    movie_titles = [movie.title for movie in writer.movies]
    print(f"Writer: {writer.first_name} {writer.last_name}, Movies: {', '.join(movie_titles)}")

# Close the database session    
db_local.close()