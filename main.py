from flask import Flask, request

from utils import get_film_by_title, get_film_by_select_years, get_film_by_rating, get_film_by_genre

app = Flask(__name__)


@app.route('/movie/<title>')
def search_title(title):
    """
    Выдает фильм по названию
    """

    result = get_film_by_title(title)

    return result


@app.route('/movie/<int:year1>/to/<int:year2>')
def search_movie_by_years(year1, year2):
    """
    Выдает список фильмов по указанному диапазону лет
    """
    result = get_film_by_select_years(year1, year2)

    return result


@app.route('/rating/children')
def movie_by_rating_children():
    """
    Список фильмов с рейтингом children: G
    """
    return get_film_by_rating('("G")')


@app.route('/rating/family')
def movie_by_rating_family():
    """
    Список фильмов с рейтингом family: "G", "PG", "PG-13"
    """
    rating = ("G", "PG", "PG-13")
    return get_film_by_rating(rating)


@app.route('/rating/adult')
def movie_by_rating_adult():
    """
    Список фильмов с рейтингом adult: "R", "NC-17"
    """
    rating = ("R", "NC-17")
    return get_film_by_rating(rating)


@app.route('/genre/<genre>')
def movie_by_genre(genre):
    """
    Принимает жанр, возвращает список фильмов по жару с
    """
    return get_film_by_genre(genre)


if __name__ == "__main__":
    app.run()