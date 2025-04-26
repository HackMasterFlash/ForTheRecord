from flask import Blueprint, redirect, url_for, render_template, flash, request, session
import json
from datetime import datetime
from .omdb_access import querry_omdb_api
from ..media.forms import MovieForm
from ..media.models import Movie, Actor, Writer
from .. import db

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    """The home page of the web app."""
    if request.method == 'POST':
        # Handle POST request
        # Access form data
        form_data = request.form
        media_title = form_data.get('Title')
        search_type = form_data.get('radioSearchSelect')
        if search_type.strip() == 'OMDB':
            # Call OMDB API with the selected search type
            # Example: Call the API with the title and search type
            # response = call_omdb_api(media_title, search_type)
            media_type = form_data.get('radioOmdbType')
            year = form_data.get('Year')
            if len(year) > 0:
                response = querry_omdb_api(media_title, type=media_type, year=year)
            else:
                response = querry_omdb_api(media_title, type=media_type)
            # Check if the response is valid
            if response.get('Response') == 'True':
                a_movie = Movie()
                a_movie.omdb_factory(response)    

                # Check if the movie is already in the local database
                inTable = db.session.query(Movie).filter(Movie.title == a_movie.title).first() 
                if inTable:
                    flash('{0} already in table'.format(a_movie.title))
                    a_movie = inTable
                session['omdb_result'] = json.dumps(response)                          
                return render_template('review.html', movie=a_movie)
            else:
                # figure out how to send flash messages
                flash("Error: When searching for {0} OMDB returned {1}".format(media_title, response.get('Error')))
            return render_template('home.html', results="Placeholder response")
        else:
            # Look up this title in the local database using SQLAlchemy
            # Example: Call the database query with the title
            # response = query_local_database(media_title)
            # Process the response and render the results
            # return render_template('results.html', results=response)
            # For now, just return a placeholder response
            return render_template('home.html', results="Placeholder response")
        # If no search type is selected, return an error message or redirect    
    else:
        # Handle GET request
        return render_template('home.html')    

@main_blueprint.route('/review', methods=['GET', 'POST'])
def review():
    """The review page of the web app."""
    
    if request.method == 'POST':
        # Handle POST request
        # Access form data
        form_data = request.form
        media_title = form_data.get('Title')

        omdb_result = json.loads(session.get('omdb_result', '{}'))
        # new_movie = session.get('movie', None)
        new_movie = Movie()
        new_movie.omdb_factory(omdb_result)
        if new_movie is None:
            flash("Error: No movie object found in Flask session.")
            return render_template('home.html')

        if new_movie.title != media_title:
            flash("Error: Flask stored OMDB Movie title {0} does not match review form movie title {1}.".format(new_movie.title, media_title))
            return render_template('home.html')
            
        new_movie.PersonalRating = int(form_data.get('PersonalRating'))
        new_movie.DateViewed = datetime.strptime(form_data.get('DateViewed'), '%Y-%m-%d')

        # Check if the movie is already in the local database
        inTable = db.session.query(Movie).filter(Movie.title == new_movie.title).first()
        if inTable:
            flash('{0} already in table'.format(new_movie.title))
        else:
            db.session.add(new_movie)
            db.session.commit()
            flash("Success: Entered {0} into local Db".format(media_title))

        session['movie'] = None        
        return render_template('home.html')
    
    # If the form is not submitted, render the review page with the form
    return render_template('review.html')
        