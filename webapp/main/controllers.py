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
                    # a_movie = inTable
                session['omdb_result'] = json.dumps(response)                          
                return render_template('review.html', movie=a_movie)
            else:
                # figure out how to send flash messages
                flash("Error: When searching for {0}, OMDB returned {1}".format(media_title, response.get('Error')))
            return render_template('home.html', results="Placeholder response")
        else:
            # Look up this title in the local database using SQLAlchemy
            inTable = db.session.query(Movie).filter(Movie.title == media_title).first() 
            if inTable:
                return redirect(url_for('main.movie_detail', movie_id=inTable.id))                
            else:
                flash("Sorry! {0} not found in local database.".format(media_title))
            return render_template('home.html')
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
            inTable.UpdateUsing(new_movie)
            db.session.commit()
        else:
            db.session.add(new_movie)
            db.session.commit()
            flash("Success: Entered {0} into local Db".format(media_title))

        session['movie'] = None        
        return render_template('home.html')
    
    # If the form is not submitted, render the review page with the form
    return render_template('review.html')
        
@main_blueprint.route('/listings', methods=['GET', 'POST'])
def listings():
    """The page lisitng contents of local db the web app."""
    # Use SQLAlchemy to query the database and get the list of movies
    # Take advantage of the pagination feature of Flask-SQLAlchemy
    # Example: Get the first 10 movies
    page_index = request.args.get('page', 1, type=int)
    page_of_movies = db.session.query(Movie).order_by(Movie.title).paginate(page=page_index, per_page=10)

    if request.method == 'POST':
        print("POST request received")
        # Handle POST request
        return render_template('home.html')

    return render_template('db_listing.html', page=page_of_movies)

@main_blueprint.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    """The page showing details of a movie."""
    # Use SQLAlchemy to query the database and get the movie details
    movie = db.session.query(Movie).get(movie_id)
    if not movie:
        flash("Error: Movie with ID {0} not found.".format(movie_id))
        return redirect(url_for('main.listings'))
    
    if request.method == 'POST':
        flash("Todo: Handle POST request for movie detail page")
        return render_template('home.html')

    return render_template('movie_detail.html', movie=movie)

@main_blueprint.route('/movie/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """Delete a movie from the database."""
    # Use SQLAlchemy to query the database and delete the movie
    movie = db.session.query(Movie).get(movie_id)
    if not movie:
        flash("Error: Movie with ID {0} not found.".format(movie_id))
        return render_template('home.html')

    # Add bootstrap modal confirmation
    # if request.method == 'POST':
    #     # Handle POST request

    db.session.delete(movie)
    db.session.commit()
    flash("Success: Deleted movie with ID {0}".format(movie_id))
    return render_template('home.html')

@main_blueprint.route('/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Edit a movie in the database."""
    # Use SQLAlchemy to query the database and get the movie details

    if request.method == 'GET':
            movie = db.session.query(Movie).get(movie_id)
            if not movie:
                flash("Error: Movie with ID {0} not found.".format(movie_id))
                return render_template('home.html')
            # Render the edit form with the movie details
            return render_template('edit_movie.html', movie=movie)
    else:
        # Handle POST request
        # Access form data
        form_data = request.form
        media_title = form_data.get('Title')
        Movie.query.filter_by(id=movie_id).first().update(
            title='New Title',
            year=2023,
            rating=8.5,
            genre='Action',
            director='New Director',
            writer='New Writer',
            actors='New Actors',
            plot='New Plot',
            poster='New Poster URL'
        )
        db.session.commit()
        flash("Success: Updated movie with ID {0}".format(movie_id))
        return render_template('home.html')


    

    