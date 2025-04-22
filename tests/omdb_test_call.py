import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_movie_data(title):
    """
    Queries the OMDb API for information about the movie "Jaws".

    Returns:
        dict: A dictionary containing the movie data from the API,
              or None if an error occurred.
    """
    api_key = os.environ.get("OMDB_API_KEY")
    if not api_key:
        print("Error: OMDB_API_KEY environment variable not set.")
        return None

    base_url = "http://www.omdbapi.com/"
    params = {
        "t": title,  # 't' parameter for movie title
        "apikey": api_key,
        "type": "movie"  # Explicitly specify we are looking for a movie
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error querying OMDb API: {e}")
        return None
    except ValueError:
        print("Error decoding JSON response from OMDb API.")
        return None

if __name__ == "__main__":
    title = "Apollo 13"
    jaws_data = get_movie_data(title)
    if jaws_data:
        if jaws_data.get("Response") == "True":
            print("Movie data for 'Jaws':")
            for key, value in jaws_data.items():
                print(f"{key}: {value}")
        else:
            print(f"Error: {jaws_data.get('Error')}")