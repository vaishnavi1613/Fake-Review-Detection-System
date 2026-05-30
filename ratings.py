import streamlit as st
import requests

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("⭐ Movie Ratings")

    try:
        response = requests.get("http://127.0.0.1:8000/movies/ratings/")
        if response.status_code == 200:
            movies = response.json()

            if not movies:
                st.info("No ratings available yet.")
            else:
                for movie in movies:
                    st.subheader(movie['title'])
                    st.write(f"Average Rating: {movie['average_rating']} ⭐")
                    st.write(f"Total Reviews: {movie['total_reviews']}")
                    st.markdown("---")
        else:
            st.error("Failed to fetch ratings.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
