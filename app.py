import streamlit as st
import pandas as pd
import pickle
import requests

# ----------------- Streamlit Setup -----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ----------------- Helper Functions -----------------

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=041444c9426917abe3524991e44e0ed6'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = new_df.iloc[i[0]].movie_id
        recommended_movie_names.append(new_df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# ----------------- Load Data -----------------

new_df = pd.read_csv('movie.csv')  # Must contain 'title' and 'movie_id' columns
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------------- UI Design -----------------

st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Discover movies similar to your favorites instantly!</p>", unsafe_allow_html=True)

selected_movie = st.selectbox('🎥 Select a Movie You Like:', new_df['title'].to_list())

if st.button('🔍 Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("## 🔥 Top 5 Recommendations Just for You")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_container_width=True)
            st.markdown(f"<h5 style='text-align: center;'>{recommended_movie_names[idx]}</h5>", unsafe_allow_html=True)
