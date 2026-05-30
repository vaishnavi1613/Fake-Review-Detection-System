import streamlit as st
import pandas as pd
import sqlite3

# Function to create the table if it doesn't exist
def create_movie_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT,
            release_year INTEGER,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to add a movie to the database
def add_movie(title, genre, release_year, description):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (title, genre, release_year, description) VALUES (?, ?, ?, ?)",
                       (title, genre, release_year, description))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"❌ Database error: {e}")
    finally:
        conn.close()

# Function to upload and parse CSV
def upload_csv_file(uploaded_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Check if the required columns exist
        required_columns = ["title", "genre", "release_year", "description"]
        if not all(col in df.columns for col in required_columns):
            st.error("❌ CSV file must contain 'title', 'genre', 'release_year', and 'description' columns.")
            return

        # Insert each movie into the database
        for index, row in df.iterrows():
            title = row["title"]
            genre = row["genre"]
            release_year = int(row["release_year"])
            description = row["description"]
            add_movie(title, genre, release_year, description)

        st.success(f"✅ {len(df)} movies uploaded successfully!")

    except Exception as e:
        st.error(f"❌ Error: {e}")

        if "user" not in st.session_state:
            st.warning("⚠️ You must be logged in to like or dislike a review.")
            st.stop()

# The show() function that will be used by Streamlit to display the page
def show():
    st.title("🎬 Upload Movies (Bulk Upload via CSV)")

    create_movie_table()  # Ensure that the movies table exists

    # Add instructions to guide users on uploading a CSV file
    st.write("""
        📥 **Bulk Upload Movies**: Upload a CSV file containing movie information.
        The CSV file should include the following columns:
        - `title`: Movie title
        - `genre`: Movie genre
        - `release_year`: Year of release
        - `description`: A brief description of the movie
    """)

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        # Show the file preview (optional)
        st.subheader("Preview of the uploaded CSV file:")
        try:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())  # Show the first 5 rows for review
        except Exception as e:
            st.error(f"❌ Error reading the CSV file: {e}")

        # Option to confirm upload
        if st.button("➕ Upload Movies from CSV"):
            upload_csv_file(uploaded_file)
