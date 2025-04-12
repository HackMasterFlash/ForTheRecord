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
movie_actor_association = Table(
    'movie_actor', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)

# Define the Movie model
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String)
    actors = relationship("Actor", secondary=movie_actor_association, back_populates="movies")

    def __repr__(self):
        return f"<Movie(title='{self.title}', director='{self.director}')>"

# Define the Actor model
class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    movies = relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __repr__(self):
        return f"<Actor(first_name='{self.first_name}', last_name='{self.last_name}')>"

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
    actor3 = Actor(first_name="Meryl", last_name="Streep")
    actor4 = Actor(first_name="Tom", last_name="Hanks")

    db.add_all([actor1, actor2, actor3, actor4])
    db.commit()

    # Create some movies and associate actors
    movie1 = Movie(title="Inception", director="Christopher Nolan", actors=[actor1, actor2])
    movie2 = Movie(title="The Departed", director="Martin Scorsese", actors=[actor1, actor3])
    movie3 = Movie(title="Forrest Gump", director="Robert Zemeckis", actors=[actor4])
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

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)
