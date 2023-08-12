from flask import Blueprint, jsonify, request
from moviewb_app.data_manager.SQLiteDataManager import SQLiteDataManager

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = data_manager.get_all_users()
    users_list = [{'user_id': user.user_id, 'name': user.name} for user in users]
    return jsonify(users_list)

# ...



@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        user_movies = [{'movie_id': movie.movie_id, 'title': movie.title} for movie in user.movies]
        return jsonify(user_movies)
    return jsonify({'message': 'User not found'}), 404


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        title = request.json.get('title')
        director = request.json.get('director')
        year = request.json.get('year')
        genre = request.json.get('genre')
        rating = request.json.get('rating')
        poster = request.json.get('poster')

        movie = data_manager.add_movie(title=title, director=director, year=year, genre=genre, rating=rating, user=user, poster=poster)

        return jsonify({'message': 'Movie added successfully', 'movie_id': movie.movie_id}), 201
    return jsonify({'message': 'User not found'}), 404
