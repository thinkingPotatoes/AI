from flask import Flask, request, make_response
from .sim_movies import recommendMovies

import joblib
import yaml
import json

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

with open('api_config.yaml', encoding='UTF8') as f:
    config = yaml.safe_load(f)

@app.route("/rating/<userId>", methods=['POST'])
def predictMovieScore(userId):
    req = request.get_json()

    userId = req['userId']
    movieIds = req['movieId']

    model = joblib.load(config['model_path'])

    pred_rating = {}
    for movieId in movieIds:
        pred_rating[movieId] = round(model.predict(userId, movieId).est, 1)

    result = {"userId": userId, "result": pred_rating}
    result = json.dumps(result, ensure_ascii=False, indent=4)
    res = make_response(result)
    return res

@app.route("/recommend/<userID>", methods=['POST'])
def recommendSimMovies(userID):
    req = request.get_json()

    userId = req['userId']
    topN = req['topN']

    result = recommendMovies(userId, topN)

    result = {"userId": userId, "result": result}
    result = json.dumps(result, ensure_ascii=False, indent=4)
    res = make_response(result)
    return res

if __name__ == '__main__':
    app.run(host="localhost", port="9000", debug=True)
