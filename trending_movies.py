# pages/trending_movies.py

import streamlit as st

# DEMO MODE: Skip backend, use fixed movie list
demo_trending_movies = [
    {
        "title": "Legally Veer",
        "description": "Veer, a lawyer, takes on the case of a man wrongfully accused of murder. Proving his innocence in the courtroom will be a daunting challenge.",

    },
    {
        "title": "Chhaava",
        "description": "The death of the mighty Chhatrapati Shivaji Maharaj, who founded and led the Maratha empire to its undefeated glory relieved the Mughals. Little did they know they would now be entering the tiger’s den by facing Shivaji’s valiant son Chhatrapati Sambhaji Maharaj.",

    }
]

def show():
    st.title("🔥 Trending Movies")
    st.markdown("Showing demo trending movies with highest number of likes.")

   
    trending_movies = demo_trending_movies

    for movie in trending_movies:
        st.subheader(movie["title"])
        st.write(f"**Total Likes:** {movie.get('total_likes', 'N/A')}")
        if "description" in movie and movie["description"]:
            st.write(movie["description"])
        st.markdown("---")
