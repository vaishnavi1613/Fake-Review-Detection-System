import streamlit as st

if "user" not in st.session_state:
    st.warning("⚠️ You must be logged in to like or dislike a review.")
    st.stop()
    
def show():
    st.title("🌍 View Remote Users")

    # Dummy data for testing
    sample_users = [
        {"username": "Akash", "email": "akash21@gmail.com", "location": "New York, USA"},
        {"username": "Sahil", "email": "sahil77@gmail.com", "location": "London, UK"},
        {"username": "Aditya", "email": "aditya26@gmail.com", "location": "Tokyo, Japan"},
        {"username": "Sakshi", "email": "sakshi159@gmail.com", "location": "Berlin, Germany"},
        {"username": "Sonali", "email": "sonali11@gmail.com", "location": "Sydney, Australia"},
    ]

    # Displaying user data
    if sample_users:
        for user in sample_users:
            st.subheader(f"👤 {user['username']}")
            st.write(f"📧 **Email:** {user['email']}")
            st.write(f"📍 **Location:** {user['location']}")
            st.markdown("---")
    else:
        st.info("No remote users found.")

