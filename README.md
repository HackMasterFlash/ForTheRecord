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