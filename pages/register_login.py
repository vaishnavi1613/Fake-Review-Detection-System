import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Your FastAPI backend URL

if "auth_action" not in st.session_state:
    st.session_state.auth_action = "Login"

def show():
    st.title("🔑 Register & Login")

    auth_action = st.radio("Select Action", ["Login", "Register"], key="auth_action")

    # ---------------- Login Section ----------------
    if auth_action == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if username and password:
                try:
                    response = requests.post(f"{API_URL}/login", json={
                        "username": username,
                        "password": password
                    })
                    if response.status_code == 200:
                        user_data = response.json()
                        st.success("✅ Login successful!")
                        st.session_state.user = user_data  # ✅ Store full user data with id, username, email
                    else:
                        st.error("❌ Invalid credentials.")
                except Exception as e:
                    st.error(f"🚫 Server Error: {e}")
            else:
                st.warning("Please enter both username and password.")

    # ---------------- Register Section ----------------
    elif auth_action == "Register":
        st.subheader("Register")
        new_username = st.text_input("New Username", key="register_username")
        new_email = st.text_input("Email", key="register_email")  # ✅ Add email input
        new_password = st.text_input("New Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif new_username and new_email and new_password:
                try:
                    response = requests.post(f"{API_URL}/register", json={
                        "username": new_username,
                        "email": new_email,  # ✅ Include email in JSON
                        "password": new_password
                    })
                    if response.status_code == 200:
                        st.success("✅ Registration successful! You can now login.")
                    else:
                        st.error("🚫 Registration failed. Username might already exist.")
                except Exception as e:
                    st.error(f"🚫 Server Error: {e}")
            else:
                st.warning("Please fill in all fields.")
