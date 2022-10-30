import sqlite3
import json


def connection_sql_base(query):
    """
     Читаем из базы netflix.db по запросу
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        return cursor.execute(query).fetchall()


def get_film_by_title(title) -> dict or None:
    """
    Возвращает информацию о фильме по названию
    """
    query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title = {title}
                    ORDER BY release_year DESC
                """
    item = connection_sql_base(query)

    if item is None:
        return "Такого фильма не найдено"

    film_info = {
        "title": item[0][0],
        "country": item[0][1],
        "release_year": item[0][2],
        "genre": item[0][3],
        "description": item[0][4]
    }
    return json.dumps(film_info)


def get_film_by_select_years(from_years, to_years):
    """
    Делает выбору фильмов по годам выпуска, принимая 2 значения от и до
    """

    query = f"""
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {from_years} AND {to_years}
                        ORDER BY release_year
                        LIMIT 100
                    """
    item = connection_sql_base(query)

    if item is None:
        return "Такого фильма не найдено"

    list_film = []
    for i in item:
        films = {
            "title": i[0],
            "release_year": i[1],
        }
        list_film.append(films)

    return json.dumps(list_film)


def get_film_by_rating(rating):
    """
    Делает выборку фильмов по заданному возрастному рейтингу
    """
    query = f"""
                        SELECT title, rating, description 
                        FROM netflix
                        WHERE rating in {rating}
                        ORDER BY release_year
                    """
    item = connection_sql_base(query)

    list_film = []
    for i in item:
        films = {
            "title": i[0],
            "rating": i[1],
            "description": i[2]
        }
        list_film.append(films)

    return json.dumps(list_film)


def get_film_by_genre(genre):
    """
    Функция, которая получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов
    """
    query = f"""
                        SELECT title, description 
                        FROM netflix
                        WHERE listed_in LIKE "%{genre}%"
                        ORDER BY release_year DESC
                        LIMIT 10
                    """
    item = connection_sql_base(query)

    list_film = []
    for i in item:
        films = {
            "title": i[0],
            "description": i[1],
        }
        list_film.append(films)

    return json.dumps(list_film)


def who_with_who(name1, name2):
    """
    Функция, которая получает в качестве аргумента имена двух актеров, сохраняет всех
    актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    """
    query = f"""
                        SELECT "cast"
                        FROM netflix
                        WHERE "cast" LIKE '%{name1}%'
                        AND "cast" LIKE '%{name2}%'
                    """
    item = connection_sql_base(query)

    list_cast = []
    dict_names = {}

    for i in item:
        i_list = i[0].split(", ")
        for name in i_list:
            if name.strip() not in dict_names.keys():
                dict_names[name] = 1
            else:
                dict_names[name] = dict_names[name] + 1

    del dict_names['Rose McIver']
    del dict_names['Ben Lamb']

    for key, value in dict_names.items():
        if value > 2:
            list_cast.append(key)

    return list_cast


def what_the_type(type, year, genre):
    """
    Функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON.
    """
    query = f"""                                        
                         SELECT title, description                  
                         FROM netflix                    
                         WHERE type = '{type}'   
                         AND release_year = '{year}'
                         AND listed_in LIKE '%{genre}%'    
                   """
    item = connection_sql_base(query)

    list_film = []
    for i in item:
        films = {
            "title": i[0],
            "description": i[1],
        }
        list_film.append(films)

    return json.dumps(list_film)