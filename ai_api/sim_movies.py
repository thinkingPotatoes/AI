import pandas as pd
import itertools
import random

from sqlalchemy import create_engine, text
import yaml

import requests
import json

def connectDB(config):
    # Connection DB
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = int(config['database']['port'])
    database = config['database']['database']

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', connect_args={'charset':'utf8'})
    conn = engine.connect()

    return conn

def recommendMovies(config, userId):
    db = connectDB(config)

    sim_user_sql = 'SELECT * FROM sim_user where userId = "' + userId + '"' 
    sim_user_df = pd.DataFrame(db.execute(text(sim_user_sql)).fetchall())

    sim_seen_movie = []

    sim_user_df.drop(['userId'], axis=1, inplace=True)
    sim_users = sim_user_df.values.tolist()

    ratings_sql = 'SELECT * FROM ratings where userId in ' + str(tuple(sim_users[0]))
    ratings_df = pd.DataFrame(db.execute(text(ratings_sql)).fetchall())

    for i in sim_users[0]:
        user_rating = ratings_df[ratings_df['userId'] == i]
        # Utilize ratings distribution of users of similar tastes
        user_rating_Q2 = user_rating['rating'].quantile(.5)
        # Extract movies rated higher than the value of Q2
        sim_seen_movie.append(list(user_rating[user_rating['rating'] >= user_rating_Q2].sort_values(ascending=False, by='rating')['movieId']))

    sim_seen_movie = list(itertools.chain(*sim_seen_movie))

    user_seen_movie = list(ratings_df[ratings_df['userId'] == userId]['movieId'])
    # Extract only recommended movies that user hasn't watched
    movieId_results = list(set(sim_seen_movie).difference(user_seen_movie))

    # Extract Movie Info
    payload = json.dumps({
        "userId": userId,
        "movieId": movieId_results
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(config['rating_url']+str(userId), headers=headers, data=payload)
    req_result = json.loads(response.text)

    result = {}
    for movieId in movieId_results:
        try:
            movie_sql = 'SELECT * FROM movie where doc_id = "' + movieId + '"'
            movie_df = pd.DataFrame(db.execute(text(movie_sql)).fetchall())
            title = movie_df['title'].values[0]
            posterUrl = movie_df['posterUrl'].values[0]
        except:
            # Not exist posterUrl
            posterUrl = ""
        result[movieId] = [req_result['result'][movieId], title, posterUrl]

    return result