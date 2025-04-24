# This script demonstrates how to use the Gemini API for movie recommendations.
import google.generativeai as genai
import os
import sys
import textwrap # For cleaner printing
from dotenv import load_dotenv

# module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# if module_path not in sys.path:
#     sys.path.insert(0, module_path)  # Add to the beginning for priority

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. "
                     "Please create a .env file with your API key.")
else:
    print("GEMINI_API_KEY found in environment variables.")
genai.configure(api_key=api_key)

# Select the model
MODEL_NAME = 'gemini-1.5-pro-latest' # Suitable for text generation tasks

# --- Helper Functions ---

def format_movie_list_for_prompt(movies):
    """Formats the list of movie dictionaries into a string for the prompt."""
    formatted_string = "Here is a list of movies the user likes:\n\n"
    for i, movie in enumerate(movies):
        formatted_string += f"--- Movie {i+1} ---\n"
        formatted_string += f"Title: {movie.get('title', 'N/A')}\n"
        formatted_string += f"Director: {movie.get('director', 'N/A')}\n"
        # Handle writers/actors which might be lists or strings
        writers = movie.get('writers', [])
        formatted_string += f"Writers: {', '.join(writers) if isinstance(writers, list) else writers if writers else 'N/A'}\n"
        actors = movie.get('actors', [])
        formatted_string += f"Actors: {', '.join(actors) if isinstance(actors, list) else actors if actors else 'N/A'}\n"
        # Wrap plot for better readability in the prompt
        plot = movie.get('plot', 'N/A')
        formatted_string += f"plot: {textwrap.fill(plot, width=80)}\n\n"
    formatted_string += "--- End of List ---"
    return formatted_string

def create_recommendation_prompt(movies_formatted_string):
    """Creates the full prompt for the Gemini API."""
    prompt = f"""
You are an expert movie recommendation engine.
Based ONLY on the following list of movies liked by a user, please recommend ONE new movie that they might enjoy.

Consider the themes, genres, directors, writers, actors, and overall tone of the provided movies to make your recommendation.

**Crucially, DO NOT recommend any of the movies already present in the list provided below.**

{movies_formatted_string}

Please output ONLY the title of the recommended movie. Do not add any extra explanation, commentary, or formatting. Just the movie title.

Recommended Movie Title:
"""
    return prompt

def get_movie_recommendation(liked_movies):
    """
    Uses the Gemini API to get a movie recommendation based on liked movies.

    Args:
        liked_movies (list): A list of dictionaries, where each dictionary
                             represents a movie with keys like 'title',
                             'director', 'writers', 'actors', 'plot'.

    Returns:
        str: The recommended movie title, or an error message.
    """
    if not liked_movies:
        return "Error: Please provide at least one movie to base recommendations on."

    try:
        # 1. Format the input movies for the prompt
        formatted_movies = format_movie_list_for_prompt(liked_movies)

        # 2. Create the full prompt
        prompt = create_recommendation_prompt(formatted_movies)
        # print(f"--- DEBUG: Generated Prompt ---\n{prompt}\n----------------------------") # Uncomment for debugging

        # 3. Initialize the model
        model = genai.GenerativeModel(MODEL_NAME)

        # 4. Generate content
        response = model.generate_content(prompt)

        # 5. Extract and clean the recommendation
        if not response.parts:
             # Handle cases where the model might have safety blocks or empty responses
             safety_ratings = getattr(response, 'prompt_feedback', None)
             if safety_ratings and safety_ratings.block_reason:
                 return f"Error: Content generation blocked due to: {safety_ratings.block_reason}"
             else:
                # Check candidate details if available
                 candidates = getattr(response, 'candidates', [])
                 if candidates and getattr(candidates[0], 'finish_reason', '') != 'STOP':
                     return f"Error: Content generation stopped unexpectedly. Reason: {getattr(candidates[0], 'finish_reason', 'Unknown')}"
                 else:
                    return "Error: Received an empty response from the API."

        recommendation = response.text.strip()

        # Basic validation: Ensure it's not one of the input titles
        input_titles = {movie.get('title', '').lower() for movie in liked_movies}
        if recommendation.lower() in input_titles:
            print(f"Warning: Model recommended an input movie ('{recommendation}'). Attempting again may yield a different result or the prompt needs adjustment.")
            # You could potentially retry here, but for simplicity, we just return it with a warning.

        return recommendation

    except Exception as e:
        return f"An error occurred during API interaction: {e}"

# --- Main Execution ---
if __name__ == "__main__":
    # --- Sample Input Data ---
    # Replace this with your actual movie data

    models_iterator = genai.list_models()

    found_models = False
    for model in models_iterator:
        found_models = True
        # List available models
    
            # --- Filter for Models Supporting Content Generation ---
        # Most common use case is 'generateContent'.
        # Other methods might include 'embedContent', 'batchEmbedContents', 'countTokens'.
        if 'generateContent' in model.supported_generation_methods:
            print(f"--- Model Name: {model.name} ---")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Supported Methods: {model.supported_generation_methods}")
            # You can access other attributes like:
            # print(f"  Input Token Limit: {model.input_token_limit}")
            # print(f"  Output Token Limit: {model.output_token_limit}")
            # print(f"  Supported Versions: {model.version}") # Might show different versions
            print("-" * (len(model.name) + 16)) # Separator line
            print() # Add a blank line for readability

    if not found_models:
        print("No models found. Check your API key and permissions.")

    user_liked_movies = [
        {
            "title": "Inception",
            "director": "Christopher Nolan",
            "writers": ["Christopher Nolan"],
            "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Tom Hardy"],
            "plot": "A thief who steals corporate secrets through use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster."
        },
        {
            "title": "The Matrix",
            "director": "Lana Wachowski, Lilly Wachowski",
            "writers": ["Lilly Wachowski", "Lana Wachowski"],
            "actors": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving"],
            "plot": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence."
        },
        {
            "title": "Blade Runner 2049",
            "director": "Denis Villeneuve",
            "writers": ["Hampton Fancher", "Michael Green"],
            "actors": ["Ryan Gosling", "Harrison Ford", "Ana de Armas", "Sylvia Hoeks"],
            "plot": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years."
        }
    ]

    print("Getting movie recommendation based on:")
    for movie in user_liked_movies:
        print(f"- {movie['title']}")
    print("\n...")

    recommendation = get_movie_recommendation(user_liked_movies)

    print("\n--- Gemini Movie Recommendation ---")
    print(recommendation)
    print("-----------------------------------")

    # --- Example with fewer details (shows robustness) ---
    print("\n\n--- Example with less detailed input ---")
    user_liked_movies_simple = [
         {
            "title": "Spirited Away",
            "director": "Hayao Miyazaki",
            "plot": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts."
        },
        {
            "title": "Howl's Moving Castle",
            "director": "Hayao Miyazaki",
            "plot": "When an unconfident young woman is cursed with an old body by a spiteful witch, her only chance of breaking the spell lies with a self-indulgent yet insecure young wizard and his companions in his legged, walking castle."
        }
    ]
    print("Getting recommendation based on:")
    for movie in user_liked_movies_simple:
        print(f"- {movie['title']}")
    print("\n...")
    recommendation_simple = get_movie_recommendation(user_liked_movies_simple)
    print("\n--- Gemini Movie Recommendation ---")
    print(recommendation_simple)
    print("-----------------------------------")