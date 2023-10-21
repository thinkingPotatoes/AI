import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy import create_engine
import yaml

import time
from ai_api.utils import createLogger

def connectDB(config):
    # Connection DB
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = int(config['database']['port'])
    database = config['database']['database']

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', connect_args={'charset':'utf8'})
    conn = engine.connect()

    return conn, engine

def find_n_neighbours(df, n):
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False).iloc[:n].index,
          index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

def sim_user_df(config):
    start_time = time.time()

    conn, engine = connectDB(config)

    sql = 'SELECT * FROM star_rating'
    ml_rating = pd.read_sql(sql, conn)

    ml_rating_mean = ml_rating.groupby(by="userId", as_index=False)['rating'].mean()
    ml_rating_avg = pd.merge(ml_rating, ml_rating_mean, on='userId')
    ml_rating_avg['adg_rating'] = ml_rating_avg['rating_x'] - ml_rating_avg['rating_y']

    final = pd.pivot_table(ml_rating_avg, values='adg_rating', index='userId', columns='movieId')

    final_movie = final.fillna(final.mean(axis=0))
    # final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)

    cosine = cosine_similarity(final_movie)
    np.fill_diagonal(cosine, 0)

    sim_with_movie = pd.DataFrame(cosine, index=final_movie.index, columns=final_movie.index)

    sim_user_df = find_n_neighbours(sim_with_movie, 10)
    # print(sim_user_df)
    # sim_user.to_csv("sim_user.csv")

    ## Store in DB (sim_user)
    sim_user_df.to_sql(name='sim_user', con=engine, if_exists='replace')
    conn.close()

    end_time = str(round(time.time() - start_time, 4))
    logger = createLogger("sim_users")
    logger.info("elapsed time : " + end_time)

    return {"status" : 200}

if __name__ == "__main__":
    with open('api_config.yaml', encoding='UTF8') as f:
        config = yaml.safe_load(f)
    sim_user_df(config)