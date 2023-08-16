import pandas as pd
import itertools
import random

from sqlalchemy import create_engine
import yaml

def connectDB():
    # Connection DB
    with open('../api_config.yaml', encoding='UTF8') as f:
        config = yaml.safe_load(f)

    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = int(config['database']['port'])
    database = config['database']['database']

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8')
    conn = engine.connect()

    return conn

def recommendMovies(userId, topN):
    conn = connectDB()
    sim_user_sql = 'SELECT * FROM sim_user'
    sim_user = pd.read_sql(sim_user_sql, conn, index_col='userId')
    ratings_sql = 'SELECT * FROM ratings'
    ratings = pd.read_sql(ratings_sql, conn)

    print(sim_user)

    sim_seen_movie = []

    top_df = sim_user.loc[userId]
    sim_users = list(top_df.values)

    for i in sim_users:
        user_rating = ratings[ratings['userId'] == i]
        user_rating_Q3 = user_rating['rating'].quantile(.75)
        sim_seen_movie.append(list(user_rating[user_rating['rating'] >= user_rating_Q3].sort_values(ascending=False, by='rating')['movieId']))

    sim_seen_movie = list(itertools.chain(*sim_seen_movie))

    user_seen_movie = list(ratings[ratings['userId'] == userId]['movieId'])
    results = list(set(sim_seen_movie).difference(user_seen_movie))

    if len(results) > topN:
        results = random.sample(results, topN)

    return results