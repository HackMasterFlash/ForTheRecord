# config.py
### This file is used to do flask configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)

# Access the environment variables using os.environ
# api_key = os.environ.get("API_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))


# This version comes from the book "Mastering Flask Web Development" by Daniel Gaspar and Jack Stouffer
class Config(object): 
    SECRET_KEY = os.environ.get("SECRET_KEY")
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
    POSTS_PER_PAGE = 10 
 
class ProdConfig(Config): 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'mydatabase.db') 
 
class DevConfig(Config): 
    # DEBUG = True
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'mydatabase.db')