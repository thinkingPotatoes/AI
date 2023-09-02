from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split

from sqlalchemy import create_engine
import yaml
import pickle

import pandas as pd

def connectDB(config):
    # Connection DB
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = int(config['database']['port'])
    database = config['database']['database']

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    conn = engine.connect()

    return conn

def ratingModel(config):
    conn = connectDB(config)

    ratings_sql = 'SELECT * FROM star_rating'
    ratings = pd.read_sql(ratings_sql, conn)

    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader=reader)

    trainset, testset = train_test_split(data, test_size=.2, random_state=42)

    algo = SVD()
    algo.fit(trainset)

    with open('./ai_core/model/movie_predict.pkl','wb') as f:
        pickle.dump(algo, f)

    return {'status':200}