# ForTheRecord
Media consumption tracking flask app

I'm trying out a bunch of technologies with this one. Obviously, Flask. Loosely following 
the Flask book from Packt publishing entitled
'Mastering Flask Web Development: second edition' by Daniel Gaspar 

Also trying out the uv python packagemenagment system.

Created virtual python environment with uv:
uv venv --python 3.13
Activate with: source .venv/bin/activate

Install packages
uv pip install <package name>

I like to use the python-dotenv package to load secret keys that I do not want to have included in a public repository.

In a .env file include your key=value collections of secrets

API_KEY=my_special_key
DEBUG=True
DB_URL=sqlite:///database.db


Then in your python code:

#
import os
from dotenv import load_dotenv

load_detenv()

DEBUG = os.environ.get("DEBUG")
API_KEY = os.environ.get("API_KEY")

OMDB Fields I want to ingest:
Title: Apollo 13
Year: 1995
Director: Ron Howard
Writer: Jim Lovell, Jeffrey Kluger, William Broyles Jr.
Actors: Tom Hanks, Bill Paxton, Kevin Bacon
Plot: NASA must devise a strategy to return Apollo 13 to Earth safely after the spacecraft undergoes massive internal damage putting the lives of the three astronauts on board in jeopardy.
Poster: https://m.media-amazon.com/images/M/MV5BMGZmNGY1OTAtNjFkYS00MjcyLWFlZjUtYzEyMDllZGZhMzM3XkEyXkFqcGc@._V1_SX300.jpg
Ratings: [{'Source': 'Internet Movie Database', 'Value': '7.7/10'}, {'Source': 'Rotten Tomatoes', 'Value': '96%'}, {'Source': 'Metacritic', 'Value': '78/100'}]
Type: movie

OMDB Database fields:
Title: Apollo 13
Year: 1995
Rated: PG
Released: 30 Jun 1995
Runtime: 140 min
Genre: Adventure, Drama, History
Director: Ron Howard
Writer: Jim Lovell, Jeffrey Kluger, William Broyles Jr.
Actors: Tom Hanks, Bill Paxton, Kevin Bacon
Plot: NASA must devise a strategy to return Apollo 13 to Earth safely after the spacecraft undergoes massive internal damage putting the lives of the three astronauts on board in jeopardy.
Language: English
Country: United States
Awards: Won 2 Oscars. 31 wins & 59 nominations total
Poster: https://m.media-amazon.com/images/M/MV5BMGZmNGY1OTAtNjFkYS00MjcyLWFlZjUtYzEyMDllZGZhMzM3XkEyXkFqcGc@._V1_SX300.jpg
Ratings: [{'Source': 'Internet Movie Database', 'Value': '7.7/10'}, {'Source': 'Rotten Tomatoes', 'Value': '96%'}, {'Source': 'Metacritic', 'Value': '78/100'}]
Metascore: 78
imdbRating: 7.7
imdbVotes: 324,064
imdbID: tt0112384
Type: movie
DVD: N/A
BoxOffice: $173,837,933
Production: N/A
Website: N/A
Response: True