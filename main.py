import streamlit as st
import pickle
import pandas as pd

import requests
def fetch_poster_path(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiNmM1N2Y4MDY4MDcyZjJhODQyODM0ZmVhNjhlZGMyNCIsIm5iZiI6MTcxMjY2NDIxNy4wOTMsInN1YiI6IjY2MTUyZTk5NTkwMDg2MDBlMzdjZGQzYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iWQne35p0PT_vTtd0b5rdfy05CwvQGV5K2nqUP5K0Co"
    }

    response = requests.get(url, headers=headers)
    data =response.json()
    poster_path= "https://image.tmdb.org/t/p/w185/"+data['poster_path']

    return poster_path


movie_list = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movie_list)
similarity = pickle.load(open('similarity.pkl','rb'))
def reccomend(movie):
    movie_id = movies[movies['title']==movie].index[0]
    distance = similarity[movie_id]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key = lambda x:x[1])[1:6]
    recommened_movies = []
    fetched_posters=[]
    for i in movie_list:
       movie_id = movies.iloc[i[0]].movie_id
       recommened_movies.append(movies.iloc[i[0]].title)
       fetched_posters.append(fetch_poster_path(movie_id))
    return recommened_movies,fetched_posters


st.title('Movie recommendation system')
selected_movie = st.selectbox(
  'All Movies',
  movies['title'].values)
st.button("Reset", type="primary")
if st.button("Recommend"):
    names,posters = reccomend(selected_movie)
    cols =st.columns(len(names))
    for i, (name,poster) in enumerate(zip(names,posters)):
        with cols[i]:
            st.text(name)
            st.image(poster)
 