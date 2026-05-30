import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()

def show():
    st.title("Like/Dislike Reviews")

    response = requests.get(f"{BACKEND_URL}/reviews/")
    if response.status_code == 200:
        reviews = response.json()
        for review in reviews:
            review_id = review["review_id"]
            movie_title = review["movie_title"]
            review_text = review["review_text"]

            st.subheader(f"🎬 {movie_title}")
            st.write(f"💬 {review_text}")

            # Get like/dislike counts
            counts = requests.get(f"{BACKEND_URL}/reviews/{review_id}/likes-dislikes/").json()
            likes = counts["likes"]
            dislikes = counts["dislikes"]

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👍 Like ({likes})", key=f"like_{review['review_id']}"):
                    requests.post(f"{BACKEND_URL}/reviews/{review_id}/likes-dislikes/", json={
                        "user_id": st.session_state.user["id"],  # Use correct user ID
                        "reaction": "like"
                    })
                    st.experimental_rerun()
                    st.success("Liked!")
            with col2:
                if st.button(f"👎 Dislike ({dislikes})", key=f"dislike_{review['review_id']}"):
                    requests.post(f"{BACKEND_URL}/reviews/{review_id}/likes-dislikes/", json={
                        "user_id": st.session_state.user["id"],
                        "reaction": "dislike"
                    })
                    st.experimental_rerun()
                    st.success("Disliked!")
    else:
        st.error("Failed to fetch reviews")
