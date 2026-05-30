import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("👤 Profile")
    st.markdown("View your profile details and activity summary.")

    # Check login state
    if "user" not in st.session_state or "id" not in st.session_state.user:
        st.warning("⚠️ You must be logged in to view your profile.")
        return


    user_id = st.session_state.user["id"]
    try:
        # Fetch user profile from FastAPI
        response = requests.get(f"{API_URL}/users/{user_id}")
        if response.status_code == 200:
            profile = response.json()
            st.subheader(f"👋 Welcome, {profile['username']}!")
            st.write(f"📧 Email: {profile['email']}")
           
        else:
            st.error("Failed to load profile.")
    except Exception as e:
        st.error(f"Error: {e}")
