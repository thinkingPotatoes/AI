from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split

from sqlalchemy import create_engine
import yaml
import pickle

import pandas as pd

import time
import logging

logger = logging.getLogger(name='predict_rating')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - RMSE & elapsed time : %(message)s')
streamHandler = logging.StreamHandler()
file_handler = logging.FileHandler('predict_rating.log', mode='a')
streamHandler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(file_handler)
    
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
    start_time = time.time()

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

    predictions = algo.test(testset)
    rmse = str(round(accuracy.rmse(predictions), 4))
    end_time = str(round(time.time() - start_time, 4))
    logger.info(rmse + " & " + end_time)

    return {'status':200}