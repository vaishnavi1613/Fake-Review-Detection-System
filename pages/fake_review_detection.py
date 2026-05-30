# fake_review_detection.py

import streamlit as st
import requests

def show():
    st.title("🤖 Fake Review Detection")
    st.markdown("Enter a movie review below to check if it's **Fake or Genuine**.")

    # 🆕 Get movie list from backend
    response = requests.get("http://localhost:8000/movies/")
    movies = response.json()

    # 🆕 Dropdown to select movie
    movie_titles = [movie['title'] for movie in movies]
    selected_title = st.selectbox("🎬 Select a Movie", movie_titles)

    # 📝 Review input
    review_text = st.text_area("✍️ Write your review here")

    if st.button("🔍 Detect"):
        if review_text.strip() and selected_title:
            movie_id = next(movie['id'] for movie in movies if movie['title'] == selected_title)

            payload = {
                "movie_id": movie_id,
                "review_text": review_text
            }

            response = requests.post("http://localhost:8000/predict_review/", json=payload)
            if response.status_code == 200:
                result = response.json()['prediction']
                label = "🟢 Genuine Review" if result == "genuine" else "🔴 Fake Review"
                st.success(f"Prediction: {label}")
            else:
                st.error("Something went wrong with the prediction.")
        else:
            st.warning("Please select a movie and enter your review.")
