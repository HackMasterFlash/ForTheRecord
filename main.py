# The entry point for my Flask web app
# The app driver code for my ForTheRecord media consuming database interface
# This will nominally be a flask app


# To start I am going to follow the "Mastering Flask Web Development" by Daniel Gaspar example and use 
# the config.py file to set up the app

# from flask import render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from models import Media

# Using connexion's spec first API approach to develop or I will later when I get to it
# app = config.connex_app
# app.add_api(config.basedir / "openapi.yml")
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return '<h1>Hello World</h1>'
    # media = Media.query.all()
    # return render_template("home.html", media=media)

# class FTR_User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)

#     def __init__(self, username):
#         self.username = username

#     def __repr__(self):
#         return f"<User {self.username}>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)