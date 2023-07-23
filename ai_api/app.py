from flask import Flask, request
from AI.ai_api.sim_movies import recommendMovies

app=Flask(__name__)

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