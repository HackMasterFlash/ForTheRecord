from flask import Blueprint, redirect, url_for, render_template, request
from .omdb_access import querry_omdb_api

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
            response = querry_omdb_api(media_title)
            # Process the response and render the results
            # return render_template('results.html', results=response)
            # For now, just return a placeholder response
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
