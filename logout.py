import streamlit as st
import time

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("🚪 Logout")

    if "user" in st.session_state:
        # Clear user session
        del st.session_state["user"]
        st.success("✅ You have been logged out successfully!")
          
    else:
        st.warning("⚠️ You are not logged in.")
