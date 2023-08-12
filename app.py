from flask import Flask, render_template, request, redirect, url_for
from data_manager.SQLiteDataManager import SQLiteDataManager
import requests
from data_manager.models import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Itay1643!'
db_path = os.path.join(app.root_path, 'data', 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)  # Initialize db here

data_manager = SQLiteDataManager(database_uri=app.config['SQLALCHEMY_DATABASE_URI'], db=db)

API_KEY = "3863e126"


@app.route('/', methods=['GET'])
def home():
    """Home Page"""
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Display a list of the selected user's favorite movies"""
    user = data_manager.get_user_by_id(user_id)
    user_movies = user.movies if user else []
    return render_template('users_movies.html', user_movies=user_movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Adds a new User to the database,
    Assigning them a new ID based on old IDs"""
    if request.method == 'POST':
        name = request.form['name']

        # Create a new Users object
        data_manager.add_user(name)

        # Redirect to the list of users
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Displays a form to add a new movie to the user's list of movies"""
    user = data_manager.get_user_by_id(user_id)

    if request.method == 'POST':
        movie_title = request.form.get('title')

        if movie_title:
            # Make a request to OMDb API
            omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"

            response = requests.get(omdb_url)
            movie_data = response.json()

            print("Movie Data:", movie_data)  # Print the retrieved movie data

            if movie_data.get('Response') == 'True':
                title = movie_data.get("Title")
                director = movie_data.get("Director")
                year = movie_data.get("Year")
                genre = movie_data.get("Genre")
                rating = movie_data.get("imdbRating")

                # Create a new movie instance
                data_manager.add_movie(title=title, director=director, year=year, genre=genre, rating=rating, user=user)

                print("Movie Added:", title)  # Print the added movie title

                # Redirect back to the user_movies page
                return redirect(url_for('user_movies', user_id=user_id))

            else:
                error_message = "Movie not found. Please enter a valid movie title."
                return render_template('add_movie.html', user_id=user_id, error_message=error_message)

        return render_template('add_movie.html', user_id=user_id)

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from the user's list of movies"""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
