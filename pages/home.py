import streamlit as st

def show():
    # Title - centered using HTML
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 3em;'>🎬 Welcome to the Fake Review Detection System</h1>
        """,
        unsafe_allow_html=True
    )

    # Subtitle - centered and larger font
    st.markdown(
        """
        <h3 style='text-align: center; color: gray; font-size: 1.5em;'>
            This system helps detect fake reviews.
        </h3>
        """,
        unsafe_allow_html=True
    )
