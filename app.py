from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def get_latest_popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    popular_movies = data['results'][:10]  # Get the first 10 popular movies
    return popular_movies

def search_movies(movie_title):
    url = f"http://www.omdbapi.com/?s={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_movie_details_by_tmdb_id(tmdb_id):
    # Get the movie details from TMDb
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    tmdb_data = response.json()
    
    # Extract the IMDb ID from the TMDb data
    imdb_id = tmdb_data.get('imdb_id')
    
    # If IMDb ID is available, use it to get detailed information from OMDb
    if imdb_id:
        return get_movie_details(imdb_id)
    else:
        return tmdb_data  # If IMDb ID is not available, return the TMDb data

def get_movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = []
    popular_movies = get_latest_popular_movies()  # Fetch latest popular movies

    if request.method == 'POST':
        movie_title = request.form['movie_title']
        search_result = search_movies(movie_title)
        if search_result.get('Response') == 'True':
            movies = search_result['Search']
        else:
            movies = []

    return render_template('index.html', movies=movies, popular_movies=popular_movies)

@app.route('/movie/<string:tmdb_id>')
def movie_detail(tmdb_id):
    movie_details = get_movie_details_by_tmdb_id(tmdb_id)
    return render_template('movie_detail.html', movie=movie_details)

if __name__ == '__main__':
    app.run(debug=True)
