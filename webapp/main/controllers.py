from flask import Blueprint, redirect, url_for, render_template, request, flash
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
                movieForm = MovieForm()                
                return render_template('review.html', form=movieForm, movie=a_movie)
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
    form = MovieForm()
    if request.method == 'POST':
        # Handle POST request
        # Access form data
        form_data = request.form
        media_title = form_data.get('Title')
        search_type = form_data.get('radioSearchSelect')
        if search_type.strip() == 'OMDB':
            # Call OMDB API with the selected search type
            response = querry_omdb_api(media_title)
            # Check if the response is valid
            if response.get('Response') == 'True':
                a_movie = Movie()
                a_movie.omdb_factory(response)
                movieForm = MovieForm()
                return render_template('review.html', form=movieForm, movie=a_movie)
            else:
                # figure out how to send flash messages
                flash("Error: {0}".format(response.get('Error')))
            return render_template('home.html', results="Placeholder response")
    if form.validate_on_submit():
        # Handle form submission
        # Access form data
        title = form.title.data
        director = form.director.data
        actors = form.actors.data.split(',')
        writers = form.writers.data
        multiple_writers = False
        if ',' in writers:
            writers = writers.split(',')
            only_one_writer = True
        year = form.year.data
        plot = form.plot.data
        poster_url = form.poster_url.data
        rating_source = form.rating_source.data
        rating = form.rating.data

        # Create a new movie object and save it to the database
        new_movie = Movie(
            title=title,
            director=director,
            year=year,
            plot=plot,
            poster_url=poster_url,
            rating_source=rating_source,
            rating=rating
        )
        
        # Add actors to the movie object and save to the database
        for actor_name in actors:            
            actor = Actor().ActorFactory(actor_name)
            inTable = db.session.query(Actor).filter(
                Actor.first_name == actor.first_name,
                Actor.last_name == actor.last_name).first()
            if not inTable:
                db.session.add(actor)
                db.session.commit()           
            new_movie.actors.append(actor)

        if multiple_writers:
            for writer_name in writers:
                writer = Writer().WriterFactory(writer_name)
                inTable = db.session.query(Writer).filter(
                    Writer.first_name == writer.first_name,
                    Writer.last_name == writer.last_name).first()
            if not inTable:
                db.session.add(writer)
                db.session.commit()
            new_movie.writers.append(writer)
        else:
            writer = Writer().WriterFactory(writers)
            inTable = db.session.query(Writer).filter(
                Writer.first_name == writer.first_name,
                Writer.last_name == writer.last_name).first()
            if not inTable:
                db.session.add(writer)
                db.session.commit()
            new_movie.writers.append(writer)


        # db.session.add(new_movie)
        # db.session.commit()

        return render_template('review.html', form=form, movie=new_movie)
    # If the form is not submitted, render the review page with the form
    return render_template('review.html', form=form)    