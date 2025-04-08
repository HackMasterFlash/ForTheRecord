# config.py
### This file is used to do flask configuration
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# import connexion
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# connex_app = connexion.App(__name__, specification_dir=basedir)

# app = connex_app.app
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'media.db'}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
# ma = Marshmallow(app)

# This version comes from the book "Mastering Flask Web Development" by Daniel Gaspar and Jack Stouffer
class Config(object): 
    SECRET_KEY = 'my_secret_key_to_change'
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAE_also_to_change"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroks_also_to_change'
    POSTS_PER_PAGE = 10 
 
class ProdConfig(Config): 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db') 
 
class DevConfig(Config): 
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')