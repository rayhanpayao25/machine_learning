# load_data.py
import csv
from movie_recommendation_app.models import Movie

def load_movies_data():
    with open('movies.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = Movie(title=row['title'], genre=row['genre'])
            movie.save()

if __name__ == "__main__":
    load_movies_data()
