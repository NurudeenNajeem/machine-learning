import streamlit as st
import pickle
import pandas as pd
import requests

# Your TMDb API key
api_key = '51209419a4faa366018a881ebe4967d5'

# Function to fetch movie poster
def fetch(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from TMDb")
    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return None
    return "https://image.tmdb.org/t/p/w500" + poster_path

# Load movies dictionary
with open('movies1_dict.pkl', 'rb') as file:
    movie_dic = pickle.load(file)
movies = pd.DataFrame(movie_dic)

# Load similarity matrix
with open('similarity1.pkl', 'rb') as file:
    similarity = pickle.load(file)
similarity = pd.DataFrame(similarity)

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:10]
    
    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        poster_url = fetch(movie_id)
        if poster_url:
            recommended_movies_poster.append(poster_url)
        else:
            recommended_movies_poster.append("https://via.placeholder.com/500?text=No+Poster+Available")

    return recommended_movies, recommended_movies_poster

st.markdown(
    """
    <style>
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .scrolling-title {
        display: inline-block;
        white-space: nowrap;
        animation: scroll 10s linear infinite;
        font-size: 3em;
        color: #FF6347;
        font-weight : bolder;
    }

    .title-container {
        overflow: hidden;
        white-space: nowrap;
    }
    </style>
    <div class="title-container">
    <div>
        Fellow ID : FE/23/92883426 </div>
        <div>Course :AI/ML  </div>
        <div>State :Ogun    </div>
        <div class="scrolling-title">
        <div>
        Movie Recommendation System</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
# st.title('COURSE ID : FE/23/92883426')

selected_movie = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)


if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    # Display in two columns
    for i in range(0, len(names), 3):
        cols = st.columns(3)
        for col, name, poster in zip(cols, names[i:i+3], posters[i:i+3]):
            with col:
                st.image(poster, use_column_width=True)
                st.text(name)
