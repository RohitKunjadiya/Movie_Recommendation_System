import joblib

df = joblib.load('Model/movies.joblib')

def movieList():
    movies = df['Title'].values.tolist()
    movie_dict = {
        'movies': movies
    }

    return movie_dict

# print(movieList()['movies'])