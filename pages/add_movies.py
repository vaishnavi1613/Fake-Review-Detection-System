import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Your FastAPI backend URL

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()

def show():
    st.title("🎬 Add Movies")

    # Movie Input Form
    with st.form("movie_form"):
        title = st.text_input("Movie Title")
        genre = st.text_input("Genre")
        release_year = st.number_input("Release Year", min_value=1880, max_value=2100, step=1)
        description = st.text_area("Movie Description")
        submit = st.form_submit_button("➕ Add Movie")

        if submit:
            if title and genre and release_year and description:
                try:
                    response = requests.post(f"{API_URL}/movies/", json={
                        "title": title,
                        "genre": genre,
                        "release_year": release_year,
                        "description": description
                    })

                    if response.status_code == 200 or response.status_code == 201:
                        st.success(f"✅ Movie '{title}' added successfully!")
                    else:
                        st.error(f"❌ Failed to add movie. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"🚫 Server Error: {e}")
            else:
                st.warning("Please fill in all fields.")

    # Optional: Display Added Movies (via backend)
    st.subheader("📜 List of Movies")
    try:
        movies_response = requests.get(f"{API_URL}/movies")
        if movies_response.status_code == 200:
            movies = movies_response.json()
            if movies:
                for movie in movies:
                    st.write(f"**🎬 {movie['title']}** ({movie['release_year']}) - *{movie['genre']}*")
                    st.caption(movie['description'])
                    st.markdown("---")
            else:
                st.info("No movies found.")
        else:
            st.warning("⚠️ Could not fetch movies from server.")
    except Exception as e:
        st.error(f"🚫 Server Error: {e}")
