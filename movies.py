from flask import make_response, abort
from config import db
from models import Directors, Movies, MoviesSchema
import datetime

def read_all():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by movie id
    :return:                json list of all movies for all directors
    """
    movies = Movies.query.order_by(db.desc(Movies.id)).limit(5)

    # Serialize the data for the response
    movie_schema = MoviesSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_top_10():
    """
    This function displays most popularity
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    movies = Movies.query.order_by(db.desc(Movies.popularity)).limit(10)

    # Serialize the data for the response
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data

def read_one(director_id, movie_id):
    """
    This function responds to a request for
    /api/directors/{director_id}/movies/{movie_id}
    with one matching movie for the associated director
    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of movie contents
    """

    # Query the database for the movie
    movie = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )
    # Was a movie found?
    if movie is not None:
        movie_schema = MoviesSchema()
        data = movie_schema.dump(movie)
        return data
    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"movie not found for Id: {movie_id} in Director Id: {director_id}")

def create(director_id, movies):
    """
    This function creates a new movie related to the passed in director id.
    :param director_id:       Id of the director the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success
    """
    # get the parent director
    directors = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    if directors is None:
        abort(404, f"director not found for Id: {director_id}")

    try:  # validate input date
        inputDate = movies['release_date']
        year, month, day = inputDate.split('-')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        abort(400, f"input format tanggal dengan benar: {inputDate}")
    # Create a movie schema instance
    schema = MoviesSchema()
    new_movie = schema.load(movies, session=db.session)
    # Add the movie to the director and database
    directors.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)

    return data, 201


def update(director_id, movie_id, movies):
    """
    This function updates an existing movie related to the passed in
    director id.
    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param movies:            The JSON containing the movie data
    :return:                200 on success
    """
    update_movies = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    try:  # validasi release date
        inputDate = movies['release_date']
        year, month, day = inputDate.split('-')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        abort(400, f"input format tanggal dengan benar: {inputDate}")

    if update_movies is not None:

        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        update.director_id = update_movies.director_id
        update.id = update_movies.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_movies)

        return data, 200

    else:
        abort(404, f"Movie not found for Id: {movie_id} in director Id: {director_id}")


def delete(director_id, movie_id):
    """
    This function deletes a movie from the movies structure
    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    movies = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # did we find a movie?
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return make_response(
            "movies {movie_id} deleted".format(movie_id=movie_id), 200
        )
    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id} with id director {director_id}")

def budgetMore(budget):
    """
    fungsi sorting by more budget, fetch semua data yang budgetnya lebih dari parameter, 
    menerima parameter budget sebagai input, return movie dan directors yang sesuai kriteria
    jika input tidak berupa integer akan mengembalikan 404
    """
    movie = (Movies.query.filter(
        Movies.budget >= budget).order_by(Movies.budget).limit(5))

    if movie is not None:
        director_schema = MoviesSchema(many=True)
        data = director_schema.dump(movie)
        return data

    else:
        abort(404, f"no data that are more than this budget : {budget}")


