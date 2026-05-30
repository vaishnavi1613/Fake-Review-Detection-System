import streamlit as st
import requests
from datetime import date

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("📝 Add a Review with Sentiment Prediction")

    # Form to submit a review
    with st.form("review_form"):
        user_id = st.number_input("👤 User ID", min_value=1, step=1)
        movie_id = st.number_input("🎬 Movie ID", min_value=1, step=1)
        review_text = st.text_area("💬 Write your review here")
        rating = st.slider("⭐ Rating", 0.0, 5.0, step=0.5)
        review_date = st.date_input("📅 Review Date", value=date.today())
        
        submitted = st.form_submit_button("Submit Review")

    if submitted:
        if not review_text.strip():
            st.warning("Please write a review before submitting.")
        else:
            review_payload = {
                "user_id": user_id,
                "movie_id": movie_id,
                "review_text": review_text,
                "rating": rating,
                "review_date": review_date.isoformat()
            }

            try:
                response = requests.post("http://localhost:8000/add_review/", json=review_payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Review added successfully!")
                    st.write(f"📌 **Predicted Sentiment:** `{result['prediction']}`")
                else:
                    st.error("❌ Failed to add review. Server error.")
                    st.json(response.json())  # Display backend error
            except Exception as e:
                st.error(f"🚫 Could not connect to server: {e}")
