import sys
import os
from dotenv import load_dotenv
from sqlalchemy import inspect

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

try:
    # Create some actors
    actor1 = Actor(first_name="Leonardo", last_name="DiCaprio")
    actor2 = Actor.ActorFactory("Brad Pitt")
    actor3 = Actor.ActorFactory("Kevin Bacon")
    actor4 = Actor(first_name="Tom", last_name="Hanks")
    actor5 = Actor(first_name="Roy", last_name="Scheider")
    actor6 = Actor(first_name="Robert", last_name="Shaw")
    actor7 = Actor(first_name="Richard", last_name="Dreyfuss")
    actor8 = Actor(first_name="Bill", last_name="Paxton")

    # Create some directors
    director1 = Director(first_name="Christopher", last_name="Nolan")
    director2 = Director(first_name="Ron", last_name="Howard")
    director3 = Director(first_name="Robert", last_name="Zemeckis")
    director4 = Director.DirectorFactory("Steven Spielberg")

    # Create some writers
    writer1 = Writer(first_name="Peter", last_name="Benchley")
    writer2 = Writer(first_name="Carl", last_name="Gottlieb")
    writer3 = Writer(first_name="Christopher", last_name="Nolan")
    writer4 = Writer(first_name="Jim", last_name="Lovell")
    writer5 = Writer(first_name="Jeffrey", last_name="Luger")
    writer6 = Writer.WriterFactory("William Broyles Jr.")

    actors_to_add = [actor1, actor2, actor3, actor4]
    something_to_commit = False
    for an_Actor in actors_to_add:
        inTable = db_local.query(Actor).filter(
            Actor.first_name == an_Actor.first_name,
            Actor.last_name == an_Actor.last_name).first()
        if inTable:
            print('Actor {0} {1} already in table'.format(an_Actor.first_name, an_Actor.last_name))
        else:
            db_local.add(an_Actor)
            something_to_commit = True

    if something_to_commit:
        db_local.commit()
        something_to_commit = False

    writers_to_add = [writer1, writer2, writer3, writer4, writer5, writer6]
    something_to_commit = False
    for a_writer in writers_to_add:
        inTable = db_local.query(Writer).filter(
            Writer.first_name == a_writer.first_name,
            Writer.last_name == a_writer.last_name).first()
        if inTable:
            print('Writer {0} {1} already in table'.format(a_writer.first_name, a_writer.last_name))
        else:
            db_local.add(a_writer)
            something_to_commit = True

    if something_to_commit:
        db_local.commit()
        something_to_commit = False

    # Create some movies and associate actors
    movie1 = Movie(title="Inception", director=director1, actors=[actor1, actor2], writers=[writer3])
    movie2 = Movie(title="Apollo 13", director=director2, 
                   actors=[actor3, actor4, actor8],
                   writers=[writer4, writer5, writer6],
                   year=1995, IsMovie=True,
                   PersonalRating=10)
    # movie3 = Movie(title="Forrest Gump", director=director3, actors=[actor4])
    movie4 = Movie(title="Jaws", director=director4, actors=[actor7,actor5,actor6], writers=[writer1,writer2])
    
    new_movies = [movie1, movie2, movie4]
    for a_movie in new_movies:
        inTable = db_local.query(Movie).filter(
            Movie.title == a_movie.title).first()
        if inTable:
            print('{0} already in table'.format(a_movie.title))
        else:
            db_local.add(a_movie)
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

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database session
    db_local.close()