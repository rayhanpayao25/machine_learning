# recommender/utils.py

import requests

def fetch_poster(movie_id):
    # Function to fetch movie poster based on movie ID
    url = "https://api.themoviedb.org/3/movie/{}?api_key=YOUR_API_KEY&language=en-US".format(movie_id)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None
    except requests.RequestException as e:
        print("Error fetching movie poster:", e)
        return None

def recommend(movie_title, movies_df, similarity_matrix):
    # Function to recommend similar movies based on a given movie title
    try:
        index = movies_df[movies_df['title'] == movie_title].index[0]
    except IndexError:
        print("Movie not found in the database")
        return [], []

    distance = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies_df.iloc[i[0]].id
        recommend_movie.append(movies_df.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommend_poster.append(poster_url)
    return recommend_movie, recommend_poster
