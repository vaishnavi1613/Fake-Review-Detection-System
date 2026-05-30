import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Update if deployed

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("🎬 View All Movies")

    try:
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            if movies:
                for movie in movies:
                    st.subheader(f"{movie['title']} ({movie['release_year']})")
                    st.write(f"**Genre:** {movie['genre']}")
                    st.write(f"**Description:** {movie['description']}")
                    st.markdown("---")
            else:
                st.info("No movies found. Add some movies first!")
        else:
            st.error("❌ Failed to fetch movies from the server.")
    except Exception as e:
        st.error(f"🚫 Server error: {e}")

if __name__ == "__main__":
    show()
