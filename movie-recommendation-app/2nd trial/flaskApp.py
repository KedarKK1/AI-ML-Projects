from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

loaded_data = pickle.load(open('movie_dataset.pkl', 'rb'))
cosine_sim = loaded_data['cosine_sim']
get_index_from_title = loaded_data['get_index_from_title']
get_title_from_index = loaded_data['get_title_from_index']



@app.route('/getCols')
def getCols():
    return (['index', 'budget', 'genres', 'homepage', 'id', 'keywords',
       'original_language', 'original_title', 'overview', 'popularity',
       'production_companies', 'production_countries', 'release_date',
       'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title',
       'vote_average', 'vote_count', 'cast', 'crew', 'director',
       'combined_features'])

@app.route('/getAllTitles')
def getAllTitles():
    df = pd.read_csv('movie_dataset.csv')['title'].tolist()  
    return df
    # return pred_model.get_all_movies_titles()


def recommend(movie_user_likes, x):
    pass


@app.route('/getRecommendation', methods=['POST'])
def getRecommendation():
    selected_option = request.json['selected_option']
    recommendations = recommend(selected_option, 5)
    return jsonify(recommendations=recommendations)


    # pred_model.recommend(data.)
    return 0


@app.route('/')
def hello():
    return render_template('helloq.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    # app.run()