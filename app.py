import streamlit as st
import importlib

# Add home page to the top
pages = {
    "Home": "home",  # NEW LINE ✅
    "Register & Login": "register_login",
    "Add Movies": "add_movies",
    "View All Movies": "view_movies",
    "Upload Movies": "upload_movies",
    "Movie Details": "movie_details",
    "Sentiment Reviews": "sentiment_reviews",
    "All Reviews": "all_reviews",
    "Ratings": "ratings",
    "Like/Dislike": "like_dislike",
    "Fake Review Detection": "fake_review_detection",
    "Remote Users": "remote_users",
    "Trending Movies": "trending_movies",
    "Profile": "profile",
    "Recommendations": "recommendations",
    "Logout": "logout"
}

# Set page title and layout
st.set_page_config(page_title="Fake Review Detection System", layout="wide")

# Sidebar navigation
selected_page = st.sidebar.radio("Select a page", list(pages.keys()))

# Dynamically import and load the selected page
page_module = f"pages.{pages[selected_page]}"
try:
    module = importlib.import_module(page_module)
    if hasattr(module, "show"):
        module.show()
    else:
        st.error(f"The page {selected_page} is missing a `show()` function.")
except ModuleNotFoundError:
    st.error(f"Page {selected_page} not found. Make sure `{pages[selected_page]}.py` exists in the `pages/` folder.")
