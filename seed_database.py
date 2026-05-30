import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, Review, User  # Make sure your models.py file has these classes

# Setup database
DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Create all tables
Base.metadata.create_all(bind=engine)

# Load the dataset
df = pd.read_csv("IMDB_Movies.csv")  # Make sure the file has 'review' and 'sentiment' columns

# -------------------------------------
# Step 1: Add multiple users
# -------------------------------------
usernames = ["alice", "bob", "charlie", "diana", "eve"]
users = []

for name in usernames:
    user = User(
        username=name,
        email=f"{name}@example.com",
        password="hashed_password"  # Replace with hashed version if needed
    )
    session.add(user)
    users.append(user)

session.commit()
user_ids = [user.id for user in users]

# -------------------------------------
# Step 2: Add multiple movies
# -------------------------------------
movie_data = [
    ("Inception", "Sci-Fi", "A mind-bending thriller about dreams", "Hollywood", 9.99),
    ("The Matrix", "Action", "A hacker discovers reality is a simulation", "Hollywood", 8.99),
    ("Parasite", "Drama", "A poor family infiltrates a rich household", "Korean", 7.99),
    ("Interstellar", "Sci-Fi", "Explorers travel through a wormhole", "Hollywood", 10.99),
    ("3 Idiots", "Comedy", "Three engineering students learn life lessons", "Bollywood", 6.99),
]

movies = []

for title, genre, description, category, price in movie_data:
    movie = Movie(
        title=title,
        genre=genre,
        description=description,
        category=category,
        price=price
    )
    session.add(movie)
    movies.append(movie)

session.commit()
movie_ids = [movie.id for movie in movies]

# -------------------------------------
# Step 3: Add random reviews (e.g., 2000)
# -------------------------------------
sampled_reviews = df.sample(n=2000, random_state=42)

for _, row in sampled_reviews.iterrows():
    review_text = str(row['review'])
    prediction = int(row['sentiment'])  # 1 = genuine, 0 = fake
    rating = random.randint(1, 5)
    review_date = datetime.now() - timedelta(days=random.randint(0, 730))

    review = Review(
        user_id=random.choice(user_ids),
        movie_id=random.choice(movie_ids),
        review_text=review_text,
        prediction=prediction,
        rating=rating,
        review_date=review_date
    )
    session.add(review)

# Final commit
session.commit()
session.close()

print("✅ Database seeded with multiple movies, users, and randomized reviews.")
