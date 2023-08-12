from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created = db.Column(db.Date, default=datetime.now().date())
    movies = db.relationship('Movies', backref='user', lazy=True)


class Movies(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Use 'users.user_id' here
    title = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    genre = db.Column(db.String)
    rating = db.Column(db.Float)


# with app.app_context():
#     db.create_all()
#
#     new_user = Users(name="Itay")
#     db.session.add(new_user)
#     db.session.commit()
#
#     # Add a movie linked to the user
#     new_movie = Movies(title="Inception", director="Christopher Nolan", year=2010, genre="Science Fiction",
#                        user=new_user, rating=8.8)
#     db.session.add(new_movie)
#     db.session.commit()
