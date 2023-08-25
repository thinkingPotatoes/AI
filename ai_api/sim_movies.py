import pandas as pd
import itertools
import random

from sqlalchemy import create_engine
import yaml

import requests
import json

def connectDB():
    # Connection DB
    with open('Ai/api_config.yaml') as f:
        config = yaml.safe_load(f)

    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = int(config['database']['port'])
    database = config['database']['database']

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', connect_args={'charset':'utf8'})
    conn = engine.connect()

    return conn

def recommendMovies(userId, topN):
    conn = connectDB()
    sim_user_sql = 'SELECT * FROM sim_user'
    sim_user = pd.read_sql(sim_user_sql, conn, index_col='userId')
    ratings_sql = 'SELECT * FROM ratings'
    ratings = pd.read_sql(ratings_sql, conn)

    sim_seen_movie = []

    top_df = sim_user.loc[userId]
    sim_users = list(top_df.values)

    for i in sim_users:
        user_rating = ratings[ratings['userId'] == i]
        # Utilize ratings distribution of users of similar tastes
        user_rating_Q2 = user_rating['rating'].quantile(.5)
        # Extract movies rated higher than the value of Q2
        sim_seen_movie.append(list(user_rating[user_rating['rating'] >= user_rating_Q3].sort_values(ascending=False, by='rating')['movieId']))

    sim_seen_movie = list(itertools.chain(*sim_seen_movie))

    user_seen_movie = list(ratings[ratings['userId'] == userId]['movieId'])
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

    response = requests.post("http://localhost:9000/rating/"+userId, headers=headers, data=payload)
    req_result = json.loads(response.text)

    result = {}
    for movieId in movieId_results:
        try:
            title_sql = 'SELECT title FROM movie where doc_id = "' + movieId + '"'
            posterUrl_sql = 'SELECT posterUrl FROM movie where doc_id = "' + movieId + '"'
            title = pd.read_sql(title_sql, conn)['title'].values[0]
            posterUrl = pd.read_sql(posterUrl_sql, conn)['posterUrl'].values[0]
        except:
            # Not exist posterUrl
            posterUrl = ""
        result[movieId] = [req_result['result'][movieId], title, posterUrl]

    return result