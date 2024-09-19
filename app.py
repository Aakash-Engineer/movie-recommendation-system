import streamlit as st
import pandas as pd
import numpy as np
import requests
from mrs.pipeline.predict import Prediction
from IPython.display import Image

# Load movie data
movies_df = pd.read_csv('artifacts/raw/movies.csv')

# Initialize prediction class
prediction = Prediction()

# Streamlit interface
st.title("Movie Recommendation System")
def fetch_movie_image(movie_id):
    images_url = []
    for id in movie_id:
        url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f5f0e091654432696b191938d11e63df'

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNWYwZTA5MTY1NDQzMjY5NmIxOTE5MzhkMTFlNjNkZiIsIm5iZiI6MTcyNjY5ODEwOS4yNDczNTcsInN1YiI6IjY2ZWI0ZmE5NWMwNTE5YTIzNGQzYWRhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EzOK_WjEgmeL1GSbSUwH_9DLb8xvl-I_Ezp42LJyFw4"
        }

        response = requests.get(url, headers=headers)
        print(response)
        image_url = 'https://image.tmdb.org/t/p/w500'+ response.json()['poster_path']
        print(image_url)
        images_url.append(image_url)
    return images_url

# function to fetch movie image url through id

def fetch_movie_image(movie_id):
    images_url = []
    for id in movie_id:
        url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f5f0e091654432696b191938d11e63df'

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNWYwZTA5MTY1NDQzMjY5NmIxOTE5MzhkMTFlNjNkZiIsIm5iZiI6MTcyNjY5ODEwOS4yNDczNTcsInN1YiI6IjY2ZWI0ZmE5NWMwNTE5YTIzNGQzYWRhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EzOK_WjEgmeL1GSbSUwH_9DLb8xvl-I_Ezp42LJyFw4"
        }

        response = requests.get(url, headers=headers)
        print(response)
        image_url = 'https://image.tmdb.org/t/p/w500'+ response.json()['poster_path']
        print(image_url)
        images_url.append(image_url)
    return images_url


    print(response.text)
# Select box for movie names
movie_name = st.selectbox("Select a movie", movies_df['title'].tolist())

# Submit button to start prediction
if st.button("Recommend Similar Movies"):
    temp_df = movies_df[movies_df['title'] == movie_name]
    index = temp_df.index[0]
    description = temp_df['tags'].values[0]
    top_movie_indices = prediction.start_prediction(description)
    
    recommended_movies = movies_df.iloc[top_movie_indices[1:]]['title'].tolist()
    recommended_movies_id = movies_df.iloc[top_movie_indices[1:]]['id'].tolist()
    print(recommended_movies_id)
    images_url = fetch_movie_image(recommended_movies_id)
    print(images_url)

    cols = st.columns(4)
    for idx, col in enumerate(cols):
        if idx < len(images_url):
            col.image(images_url[idx], use_column_width=True)