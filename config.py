# config.py

### This file is used to do flask configuration
# This version was from something I started so long ago that I don't remember where I got it from
import pathlib
# import connexion
# from flask_sqlalchemy import SQLAlchemy

# from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
# connex_app = connexion.App(__name__, specification_dir=basedir)

# app = connex_app.app
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'media.db'}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
# ma = Marshmallow(app)

# This version comes from the book "Mastering Flask Web Development" by Daniel Gaspar and Jack Stouffer
class Config(object): 
    pass 
 
class ProdConfig(Config): 
    pass 
 
class DevConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  f"sqlite:///{basedir / 'media.db'}"