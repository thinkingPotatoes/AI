from flask import Flask, request, make_response
from .sim_movies import recommendMovies
from ai_core.extract_keywords import extractKeywords as keybert

import joblib
import yaml
import json

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

with open('api_config.yaml', encoding='UTF8') as f:
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

@app.route("/blogs/keyword/<articleId>", methods=['POST'])
def extractKeywords(articleId):
    req = request.get_json()

    articleId = req['articleId']
    review = req['review']

    keywords = keybert(review)

    result = {"articleId": articleId, "result": keywords}

    result = json.dumps(result, ensure_ascii=False, indent=4)
    res = make_response(result)
    return res

if __name__ == '__main__':
    app.run(host="localhost", port="9000", debug=True)
