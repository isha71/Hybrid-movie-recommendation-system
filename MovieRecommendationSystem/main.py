import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

EN = "en"
HI = "hi"

en_ib_item_similarity_df = pd.read_csv("english_itemBased.csv", index_col=0)
en_ub_item_similarity_df = pd.read_csv("english_userBased.csv", index_col=0)
hi_ib_item_similarity_df = pd.read_csv("hindi_itemBased.csv", index_col=0)
hi_ub_item_similarity_df = pd.read_csv("hindi_userBased.csv", index_col=0)

en_ib_item_similarity_df.columns = en_ib_item_similarity_df.columns.str.lower()
en_ub_item_similarity_df.columns = en_ub_item_similarity_df.columns.str.lower()
hi_ib_item_similarity_df.columns = hi_ib_item_similarity_df.columns.str.lower()
hi_ub_item_similarity_df.columns = hi_ub_item_similarity_df.columns.str.lower()

app = Flask(__name__)
CORS(app)


def get_user_based_data(query, language):
    try:
        similar_score = None
        if language == EN:
            similar_score = en_ub_item_similarity_df[query]
        if language == HI:
            similar_score = hi_ub_item_similarity_df[query]

        print(similar_score)

        if similar_score is not None:
            api_recommendations = similar_score.to_list()
        else:
            api_recommendations = []
    except Exception as e:
        api_recommendations = []
    return api_recommendations


def get_item_based_data(query, language):
    try:
        similar_score = None

        if language == EN:
            similar_score = en_ib_item_similarity_df[query]
        if language == HI:
            similar_score = hi_ib_item_similarity_df[query]

        if similar_score is not None:
            api_recommendations = similar_score.to_list()
        else:
            api_recommendations = []
    except:
        api_recommendations = []
    return api_recommendations


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/movie-api", methods=["POST"])
def make_rec():
    if request.method == "POST":
        data = request.json
        movie = data["movie_title"]
        # curl -X POST http://0.0.0.0:80/recms -H 'Content-Type: application/json' -d '{"movie_title":"Heat (1995)"}'
        try:
            movie = str(movie).lower()
            en_ub = get_user_based_data(movie, EN)
            en_ib = get_item_based_data(movie, EN)
            hi_ub = get_user_based_data(movie, HI)
            hi_ib = get_item_based_data(movie, HI)

            api_recommendations = {
                "en_ub_rec_movies": en_ub,
                "en_ib_rec_movies": en_ib,
                "hi_ub_rec_movies": hi_ub,
                "hi_ib_rec_movies": hi_ib
            }
            print(api_recommendations)
        except Exception as e:
            api_recommendations = {
                "en_ub_rec_movies": [],
                "en_ib_rec_movies": [],
                "hi_ub_rec_movies": [],
                "hi_ib_rec_movies": []
            }
        return api_recommendations


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
