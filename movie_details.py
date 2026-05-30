import streamlit as st
import requests
from datetime import datetime

st.title("🎬 Movie Details")

FASTAPI_URL = "http://localhost:8000"

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()

def get_movie_details(movie_id):
    response = requests.get(f"{FASTAPI_URL}/movies/{movie_id}/")
    if response.status_code == 200:
        return response.json()
    return None

def add_review(movie_id, user_id, review_text, rating):
    review_data = {
        "movie_id": movie_id,
        "user_id": user_id,
        "review_text": review_text,
        "rating": rating,
        "review_date": datetime.now().isoformat()
    }
    response = requests.post(f"{FASTAPI_URL}/reviews/", json=review_data)
    if response.status_code == 200:
        return response.json()
    return None

def show():
    movie_id = st.number_input("Enter Movie ID to view details", min_value=1, step=1)
    movie = get_movie_details(movie_id)

    if movie:
        st.subheader(f"{movie['title']} 🔗")
        st.markdown(f"**Genre:** {movie['genre']}")
        st.markdown(f"**Release Year:** {movie.get('year', 'N/A')}")
        st.markdown(f"**Description:** {movie['description']}")

        st.markdown("---")
        st.subheader("📝 Add your Review")

        review_text = st.text_area("Write your review here...")
        rating = st.slider("Rate the Movie", 1, 5, 3)

        if st.button("Submit Review"):
            user_id = st.session_state.get("user_id")
            if not user_id:
                st.error("❌ You must be logged in to submit a review.")
            elif not review_text.strip():
                st.error("❌ Please write a review before submitting.")
            else:
                result = add_review(movie_id, user_id, review_text, rating)
                if result:
                    st.success("✅ Review added successfully!")
                    st.info(f"🧠 Prediction: {result['prediction']}")
                else:
                    st.error("❌ Failed to add review.")

        st.markdown("---")
        st.subheader("🗣️ Existing Reviews")

        if movie['reviews']:
            for rev in movie['reviews']:
                st.markdown(f"**👤 {rev['username']}**")
                st.markdown(f"> {rev['review_text']}")
                st.markdown(f"⭐ Rating: {rev['rating']} | 📅 {rev['review_date']} | 🔍 Prediction: {rev['prediction']}")
                st.markdown("---")
        else:
            st.info("No reviews yet for this movie.")

    else:
        st.warning("Enter a valid Movie ID to view details.")
