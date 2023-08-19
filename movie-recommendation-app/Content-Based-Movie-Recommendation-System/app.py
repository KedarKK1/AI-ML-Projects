from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import json

app = Flask(__name__)

# loaded_data = pickle.load(open('movie_dataset.pkl', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pkl', 'rb'))
# get_all_movies_titles = pickle.load(open('get_all_movies_titles.pkl', 'rb'))
# get_index_from_title = pickle.load(open('get_index_from_title.pkl', 'rb'))
# recommend = pickle.load(open('recommend.pkl', 'rb'))
# cosine_sim = loaded_data['cosine_sim']
# get_index_from_title = loaded_data['get_index_from_title']
# get_title_from_index = loaded_data['get_title_from_index']
df = pd.read_csv('movie_dataset.csv')


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


@app.route('/getCols')
def getCols():
    return (['index', 'budget', 'genres', 'homepage', 'id', 'keywords',
             'original_language', 'original_title', 'overview', 'popularity',
             'production_companies', 'production_countries', 'release_date',
             'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title',
             'vote_average', 'vote_count', 'cast', 'crew', 'director',
             'combined_features'])


@app.route('/getAllTitles', methods=['GET'])
def getAllTitles():
    # print(cosine_sim)
    # return 0
    df = pd.read_csv('movie_dataset.csv')['title'].tolist()
    jsonString = json.dumps(df)

    return jsonString
    # return pred_model.get_all_movies_titles()


# def recommend(movie_user_likes, x):
#     pass


@app.route('/getRecommendation', methods=['POST'])
def getRecommendation():
    movie_user_likes = request.json['selected_option']
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[
        1:]  # sort movies most likely by descresing order
    i = 0
    # print("Top " + str(x) + " similar movies to "+movie_user_likes+" are:\n")
    print("Top " + str(5) + " similar movies to "+movie_user_likes+" are:\n")
    # x = int(x)
    x = 5
    ans = []
    for element in sorted_similar_movies:
        print(get_title_from_index(element[0]))
        ans.append(get_title_from_index(element[0]))
        i += 1
        if(i > x):
            break
    # return jsonify(recommendations=recommendations)\
    ans2 = json.dumps(ans)
    return render_template("frontend.html", prediction_text="Recommended movies are:- {} ".format(ans2))

    # pred_model.recommend(data.)
    # return 0


@app.route('/getRecommendation2', methods=['POST'])
def getRecommendation2():
    movie_user_likes = request.json['selected_option']
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[
        1:]  # sort movies most likely by descresing order
    i = 0
    # print("Top " + str(x) + " similar movies to "+movie_user_likes+" are:\n")
    print("Top " + str(5) + " similar movies to "+movie_user_likes+" are:\n")
    # x = int(x)
    x = 5
    ans = []
    for element in sorted_similar_movies:
        print(get_title_from_index(element[0]))
        ans.append(get_title_from_index(element[0]))
        i += 1
        if(i > x):
            break
    # return jsonify(recommendations=recommendations)\
    # ans2 = json.dumps(ans)
    return jsonify(recommendations=ans)

    # pred_model.recommend(data.)
    # return 0


@app.route('/')
def hello():
    return render_template('frontend.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    # app.run()
