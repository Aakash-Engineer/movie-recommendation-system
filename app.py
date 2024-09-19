import streamlit as st
import pandas as pd
import numpy as np
import requests
from mrs.pipeline.predict import Prediction

# Load movie data
movies_df = pd.read_csv('artifacts/raw/movies.csv')

# Initialize prediction class
prediction = Prediction()

# Streamlit interface with a centered title
st.markdown("<h1 style='text-align: center; color: #FF6347;'>🎬 Movie Recommendation System 🍿</h1>", unsafe_allow_html=True)
st.markdown("---")

def fetch_movie_image(movie_id):
    images_url = []
    for id in movie_id:
        url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f5f0e091654432696b191938d11e63df'

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNWYwZTA5MTY1NDQzMjY5NmIxOTE5MzhkMTFlNjNkZiIsIm5iZiI6MTcyNjY5ODEwOS4yNDczNTcsInN1YiI6IjY2ZWI0ZmE5NWMwNTE5YTIzNGQzYWRhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EzOK_WjEgmeL1GSbSUwH_9DLb8xvl-I_Ezp42LJyFw4"
        }

        response = requests.get(url, headers=headers)
        image_url = 'https://image.tmdb.org/t/p/w500' + response.json()['poster_path']
        images_url.append(image_url)
    return images_url

# Select box for movie names
st.markdown("<h3 style='text-align: left; color: #4CAF50;'>Select a movie to get recommendations</h3>", unsafe_allow_html=True)
movie_name = st.selectbox("", movies_df['title'].tolist())

# Submit button to start prediction
if st.button("🔍 Recommend Similar Movies"):
    temp_df = movies_df[movies_df['title'] == movie_name]
    index = temp_df.index[0]
    description = temp_df['tags'].values[0]

    top_movie_indices = prediction.start_prediction(description)

    recommended_movies = movies_df.iloc[top_movie_indices[1:]]['title'].tolist()
    recommended_movies_id = movies_df.iloc[top_movie_indices[1:]]['id'].tolist()
    images_url = fetch_movie_image(recommended_movies_id)

    # Display recommendations with a more structured layout
    st.markdown("<h2 style='text-align: left; color: #FF6347;'>Recommended Movies</h2>", unsafe_allow_html=True)
    st.markdown("---")

    for idx, movie_id in enumerate(recommended_movies_id):
        movie_details = movies_df[movies_df['id'] == movie_id].iloc[0]
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(images_url[idx], use_column_width=True)
        
        with col2:
            st.markdown(f"### {movie_details['title']}")
            st.markdown(f"**Year**: {movie_details['release_date']}")
            st.markdown(f"**Genres**: {movie_details['genres']}")
            st.markdown(f"**Overview**: {movie_details['overview'][:150]}...")  # Truncate for cleaner look
            st.markdown(f"**Crew**: {movie_details['crew']}")

        st.markdown("---")  # Divider for each movie recommendation
