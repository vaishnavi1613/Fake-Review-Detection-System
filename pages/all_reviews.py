import streamlit as st
import requests

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()

def show():
    st.title("📝 View All Movie Reviews")

    api_url = "http://127.0.0.1:8000/reviews/"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            reviews = response.json()

            #st.write("🔍 Raw API Response:", reviews)

            if not reviews:
                st.info("No reviews available.")
                return

            # Filter out reviews missing movie titles
            movie_titles = sorted(list(set(
                review["movie_title"] for review in reviews if review["movie_title"]
            )))

            selected_movie = st.selectbox("🎬 Filter by Movie:", ["All"] + movie_titles)
            st.subheader(f"Showing Reviews for: {selected_movie}" if selected_movie != "All" else "All Movie Reviews")

            found = False  # Flag to check if any matching review exists

            for review in reviews:
                movie = review.get("movie_title")
                user = review.get("username")
                text = review.get("review_text")

                # Only skip if movie or review text is missing
                if not movie or not text:
                   continue
                

                if selected_movie == "All" or movie == selected_movie:
                    found = True
                    st.markdown(f"### 🎬 {movie}")
                    st.write(f"👤 **User:** {user}")
                    st.write(f"💬 **Review:** {text}")
                    st.write(f"⭐ **Rating:** {review.get('rating', 'N/A')}")
                    st.write(f"🔍 **Prediction:** {review.get('prediction', 'N/A')}")
                    st.write(f"🕒 **Date:** {review.get('review_date', 'N/A')}")
                    st.markdown("---")

            if not found:
                st.warning("No detailed reviews available for this movie.")

        else:
            st.error(f"❌ Failed to fetch reviews. Status code: {response.status_code}")

    except Exception as e:
        st.error(f"🚫 Error fetching reviews: {e}")
