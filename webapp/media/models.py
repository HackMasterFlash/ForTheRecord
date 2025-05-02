import datetime
from .. import db

# Define the association table for the many-to-many relationship between Movie and Actor
movie_actor_association = db.Table(
    'movie_actor', db.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

# Define the association table for the many-to-many relationship between Movie and Director
movie_writer_association = db.Table(
    'movie_writer', db.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('writer_id', db.Integer, db.ForeignKey('writers.id'), primary_key=True)
)

# Define the Movie model
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True, nullable=False)
    director = db.relationship("Director", back_populates="movies")
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    writers = db.relationship("Writer", secondary=movie_writer_association, back_populates="movies")
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
    
    def writers_to_string(self):
        result = ""
        if len(self.writers) == 1:
            result = "{0} {1}".format(self.writers[0].first_name,self.writers[0].last_name)
        else:
            for i, writer in enumerate(self.writers):
                if i == 0:
                    result = "{0} {1}".format(writer.first_name,writer.last_name)
                else:
                    result = "{0}, {1} {2}".format(result, writer.first_name, writer.last_name)
        return result
    
    def omdb_factory(self, omdb_data):
        """
        Populate the movie object fields with data from the OMDB API response.

        Args:
            omdb_data (dict): The OMDB API response data.
        """
        self.title = omdb_data.get('Title')
        director_name = omdb_data.get('Director')
        if "N/A" in director_name:
            director_name = None
        if director_name:
            self.director = Director.DirectorFactory(director_name)
        else:
            self.director = None        
        actors_str = omdb_data.get('Actors')
        actors_array = []
        for each_actor in actors_str.split(','):
            an_actor = Actor.ActorFactory(each_actor)
            actors_array.append(an_actor)
        self.actors = actors_array
        writers_str = omdb_data.get('Writer')
        writers_array = []
        for each_writer in writers_str.split(','):
            a_writer = Writer.WriterFactory(each_writer)
            writers_array.append(a_writer)
        self.writers = writers_array
        self.year = omdb_data.get('Year')
        self.IsMovie = (omdb_data.get('Type') == 'movie')
        self.plot = omdb_data.get('Plot')
        self.PosterURL = omdb_data.get('Poster')
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
                    if '%' in self.RatingValueString:
                        self.RatingValue = float(self.RatingValueString.replace('%','')) / 100
                    break
            if self.RatingSource is None:
                for rating in the_ratings:
                    if rating.get('Source') == 'Internet Movie Database':
                        self.RatingSource = 'IMDb'
                        self.RatingValueString = rating.get('Value')
                        if '/' in self.RatingValueString:
                            self.RatingValue = float(self.RatingValueString.split('/')[0]) / float(self.RatingValueString.split('/')[1])
                        break
        else:
            self.RatingSource = None
            self.RatingValueString = None
    
    def UpdateUsing(self, other_movie):
        """
        Update the movie object fields with data from another version of this movie class.

        Args:
            other_movie (object): another movie class instance.
        """
        if self.title not in other_movie.title:
            raise ValueError("The title of the movie does not match the title of the other movie.")            

        if self.director == None:
            self.director = other_movie.director
        if self.writers == None:
            self.writers = other_movie.writers
        if self.actors == None:
            self.actors = other_movie.actors
        if self.year == None:
            self.year = other_movie.year
        if self.IsMovie == None:
            self.IsMovie = other_movie.IsMovie
        if self.plot == None:
            self.plot = other_movie.plot
        if self.PosterURL == None:
            self.PosterURL = other_movie.PosterURL
        if self.RatingSource == None:
            self.RatingSource = other_movie.RatingSource
        if self.RatingValue == None:
            self.RatingValue = other_movie.RatingValue
        if self.RatingValueString == None:
            self.RatingValueString = other_movie.RatingValueString
        if self.PosterLocalURL == None:
            self.PosterLocalURL = other_movie.PosterLocalURL
        if self.DateViewed == None:
            self.DateViewed = other_movie.DateViewed
        if self.PersonalRating == None:
            self.PersonalRating = other_movie.PersonalRating
        if self.Source == None:
            self.Source = other_movie.Source
        

# Define a base person class to stay dry
class Person():
    @classmethod
    def define_from_fullname(cls, fullname_str):
        last_name = ""
        first_name = ""
        full_name = fullname_str.split(' ')
        if len(full_name) > 1:
            last_name=full_name[-1]
            if cls.is_an_add_on_title(last_name):
                last_name=' '.join(full_name[-2:]).strip()
                first_name=' '.join(full_name[:-2]).strip()
            else:            
                first_name=' '.join(full_name[:-1]).strip()
        else:
            last_name=fullname_str
        return [first_name, last_name]

    @staticmethod
    def is_an_add_on_title(last_name):
        is_add_on = False
        add_ons = ["Jr", "Junior", "Sr", "Senior"]
        for add_on in add_ons:
            if add_on in last_name:
                is_add_on = True
        return is_add_on

# Define the Actor model
class Actor(db.Model, Person):
    __tablename__ = 'actors'
    __table_args__ = (db.UniqueConstraint('first_name', 'last_name', name='unique_actor'),)
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True) 
    movies = db.relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def ActorFactory( full_name_str):
        an_Actor = Actor()
        [first, last] = Actor.define_from_fullname(full_name_str)
        an_Actor.first_name = first
        an_Actor.last_name = last
        return an_Actor
        
        
# Define the Actor model
class Writer(db.Model, Person):
    __tablename__ = 'writers'
    __table_args__ = (db.UniqueConstraint('first_name', 'last_name', name='unique_actor'),)
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", secondary=movie_writer_association, back_populates="writers")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def WriterFactory( full_name_str):
        a_writer = Writer()
        [first, last] = Writer.define_from_fullname(full_name_str)
        a_writer.first_name = first
        a_writer.last_name = last
        return a_writer


# Define the Director model
class Director(db.Model, Person):
    __tablename__ = 'directors'
    __table_args__ = (db.UniqueConstraint('first_name', 'last_name', name='unique_actor'),)
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, index=True)
    movies = db.relationship("Movie", back_populates="director")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def DirectorFactory( full_name_str):
        a_director = Director()
        [first, last] = Director.define_from_fullname(full_name_str)
        a_director.first_name = first
        a_director.last_name = last
        return a_director