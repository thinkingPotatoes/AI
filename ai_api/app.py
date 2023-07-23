from flask import Flask, request
from AI.ai_api.sim_movies import recommendMovies

import joblib
import yaml

app=Flask(__name__)

with open('../api_config.yaml', encoding='UTF8') as f:
    config = yaml.safe_load(f)

@app.route("/rating/<movieId>", methods=['POST'])
def predictMovieScore(movieId):
    req = request.get_json()

    userId = req['userId']
    movieId = req['movieId']

    model = joblib.load(config['model_path'])
    pred_rating = model.predict(userId, movieId).est

    result = {"userId": userId, "movieId": movieId, "rating": pred_rating}
    return result

@app.route("/recommend/<userID>", methods=['POST'])
def recommendSimMovies(userID):
    req = request.get_json()

    userId = req['userId']
    topN = req['topN']

    results = recommendMovies(userId, topN)

    result = {"userId": userId, "results": results}
    return result

if __name__ == '__main__':
    app.run(host="localhost", port="9000", debug=True)
