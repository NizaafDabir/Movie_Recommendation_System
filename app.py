import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('moves.pkl','rb'))
similarity = pickle.load(open('similarity_score.pkl','rb'))

def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0529abd24917f4a1d64ddd00d6c6f2d3&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_posters(movie_id))

    return recommended_movies , recommended_movies_poster

movies = movies_list['title'].values

st.title('Movie Recommendation System')

Selected_movie_name = st.selectbox(
    'Select a movie',
    movies
)

if st.button('Recommend'):
    names , posters = recommend(Selected_movie_name)
    
    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])