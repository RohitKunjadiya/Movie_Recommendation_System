from flask import Flask, render_template, request
import movies_data
import joblib

movies = joblib.load("Model/movies.joblib")
similarity = joblib.load("Model/similarity.joblib")

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    x = movies.sample(12)
    return render_template('index.html',
                           title="Movie Recommendation System",
                           movie_name = x['Title'].to_list(),
                           director_name = x['Director'].to_list(),
                           cast = x['Cast'].to_list(),
                           genre = x['Genre'].to_list(),
                           image = x['Poster'].to_list(),
                           body_title = 'Movies')

def moviesName():
    moviesList = movies_data.movieList()['movies']

    return moviesList


@app.route("/recommend")
def recommend_ui():
    moviesList = moviesName()
    return render_template("recommend.html",
                           title="Recommendation System",
                           body_title="Select Movie",mlist=moviesList)


@app.route("/recommend_movies", methods=['GET','POST'])
def recommend():
    try:
        moviesList = moviesName()
        user_input = request.form.get("user_input")
      
        index = movies[movies['Title'] == user_input].index[0]
        distances = similarity[index]
        similar_items = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

        data = []
        for i in similar_items:
            item = []
            temp_df = movies[movies['Title'] == movies.iloc[i[0]]['Title']]

            item.append(temp_df['Title'].values[0])
            item.append(temp_df['Director'].values[0])
            item.append(temp_df['Cast'].values[0])
            item.append(temp_df['Genre'].values[0])
            item.append(temp_df['Poster'].values[0])

            data.append(item)

        # print(data)

        return render_template("recommend.html", title="Recommendation System",
                               body_title="Recommended Movies",
                               data=data,mlist=moviesList)

    except Exception as e:
        if user_input == '-- Choose a Movie --':
            return render_template("recommend.html", error_message="Please Select a Movie",
                               title="Recommendation System",
                               body_title="Recommended Movies",
                               mlist=moviesList)

if __name__ == "__main__":
    app.run(debug=True)