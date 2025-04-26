import os
import json
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


tfidf_vectorizer = TfidfVectorizer(stop_words='english')

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'movie_dataset.json')

with open('movie_dataset.json', 'r') as file:
    movie_data = json.load(file)
descriptions = [movie.get('description', '') for movie in movie_data]


filtered_descriptions = []
for movie in movie_data:
    description = movie.get('description', '')
    if any(word.strip() for word in description.split() if word.lower() not in tfidf_vectorizer.get_stop_words()):
        filtered_descriptions.append(description)


if not filtered_descriptions:
    print("No valid movie descriptions found after filtering.")
else:
    tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_descriptions)

   
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

@login_required(login_url='index')
def HomePage(request):
    selected_genre = request.POST.get('genre', 'All')  
    with open('movie_dataset.json', 'r') as file:
        movie_data = json.load(file)
    if selected_genre != 'All':
        recommended_movies = [movie for movie in movie_data if selected_genre in movie.get('genre', [])]
    else:
        recommended_movies = movie_data
    return render(request, 'home.html', {'recommended_movies': recommended_movies, 'selected_genre': selected_genre})

 
def get_recommendations(title, cosine_sim=None, movie_data=None):
    if cosine_sim is None:
        if movie_data is None:
            movie_data = json.load(open(json_file_path, 'r'))

        indices = {movie['title']: idx for idx, movie in enumerate(movie_data)}
        idx = indices.get(title)
        if idx is None:
            return []  

        tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_descriptions)
 
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = {movie['title']: idx for idx, movie in enumerate(movie_data)}
    idx = indices.get(title)
    if idx is None:
        return []  
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  
    movie_indices = [i[0] for i in sim_scores]
    return [movie_data[i]['title'] for i in movie_indices]

def LoginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            return HttpResponse("Your Password and Confirm Password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()

    return render(request, 'login.html')

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)  
            return redirect('home')
        else:
            return HttpResponse("Username or Password is Incorrect!")
        
    return render(request, 'index.html')
        
def LogoutPage(request):
    logout(request)
    return redirect('index')
 