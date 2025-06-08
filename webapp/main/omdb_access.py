# define a method to access the OMDB API and return the results
# import the necessary libraries
import requests
# import json
# import os
# from dotenv import load_dotenv
from flask import current_app

# load the environment variables from the .env file
# load_dotenv()
# get the API key from the environment variables
# OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def querry_omdb_api(title, type="movie", year=None):
    """
    Queries the OMDb API for information about a movie.

    Returns:
        dict: A dictionary containing the movie data from the API,
              or None if an error occurred.
    """
    api_key = current_app.config.get("OMDB_API_KEY")
    if not api_key:
        print("Error: OMDB_API_KEY environment variable not set.")
        return None

    base_url = "http://www.omdbapi.com/"
    params = {
        "t": title,  # 't' parameter for movie title
        "apikey": api_key,
        "type": type  # Explicitly specify we are looking for a movie
    }

    if year:
        params["year"] = year

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        error_explanation = f"Error querying OMDb API: {e}"
        print(error_explanation)
        return error_explanation
    except ValueError:
        print("Error decoding JSON response from OMDb API.")
        return None