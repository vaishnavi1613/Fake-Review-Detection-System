import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def show():
    st.title("🎯 Recommended Movies")
    st.markdown("Here are the top movies based on genuine user reviews or fallback suggestions:")

    try:
        response = requests.get(f"{API_URL}/recommended_movies/")
        if response.status_code == 200:
            movies = response.json()
            if movies:
                for movie in movies:
                    st.subheader(f"🎬 {movie['title']}")
                    st.write(f"🎭 Genre: {movie['genre']}")
                    st.write(f"⭐ Average Rating: {movie['avg_rating']}")
                    st.write(f"✅ Genuine Reviews: {movie['genuine_reviews']}")
                    st.markdown("---")
            else:
                st.info("No recommendations available at the moment.")
        else:
            st.error("Failed to load recommended movies.")
    except Exception as e:
        st.error(f"Error: {e}")
