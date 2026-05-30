from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from typing import List
import logging
import joblib
from schemas import ReviewResponse
from fastapi.responses import JSONResponse
from sqlalchemy import func
from schemas import MovieRatingResponse
from models import Like, Review, ReviewReaction


from database import get_db, SessionLocal
from models import Movie, Review, User
from schemas import (
    UserCreate, UserLogin, MovieCreate, ReviewCreate,
    ReviewResponse, MovieResponse, ReviewText, PredictionResponse, ReactionCreate
)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the vectorizer and SVM model
vectorizer = joblib.load("vectorizer.pkl")
svm_model = joblib.load("svm_model.pkl")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password Utilities
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Register
@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User registered successfully!",
        "user_id": new_user.id,
        "username": new_user.username
    }

# ✅ Login
@router.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {
        "message": f"Welcome, {db_user.username}!",
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email 
    }

# ✅ Get user profile by ID
@router.get("/users/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the profile info
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

# ✅ Add Movie
@router.post("/movies/", response_model=MovieResponse)
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(
        title=movie.title,
        genre=movie.genre,
        release_year=movie.release_year,
        description=movie.description
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# ✅ Get Movies
@router.get("/movies/")
def get_all_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


# ✅ Ratings 
@router.get("/movies/ratings/", response_model=List[MovieRatingResponse])
def get_movie_ratings(db: Session = Depends(get_db)):
    results = (
        db.query(
            Movie.id,
            Movie.title,
            func.avg(Review.rating).label("avg_rating"),
            func.count(Review.id).label("total_reviews")
        )
        .join(Review, Review.movie_id == Movie.id)
        .group_by(Movie.id)
        .order_by(func.avg(Review.rating).desc())
        .all()
    )
  
    return [
        {
            "movie_id": r.id,
            "title": r.title,
            "average_rating": float(round(r.avg_rating, 2)) if r.avg_rating is not None else 0.0,
            "total_reviews": r.total_reviews
        } for r in results
    ]


# ✅ Trending Movies
@router.get("/movies/trending-movies/")
def get_trending_movies(db: Session = Depends(get_db)):
    try:
        trending = db.query(
            Movie.id,
            Movie.title,
            Movie.description,
            func.count(Review.id).label("review_count"),
            func.coalesce(func.sum(Review.likes), 0).label("likes")
        ).join(Review, Review.movie_id == Movie.id)\
         .group_by(Movie.id)\
         .order_by(func.count(Review.id).desc())\
         .limit(10)\
         .all()

        # Convert to dict for safe JSON serialization
        result = []
        for row in trending:
            result.append({
                "id": row.id,
                "title": row.title,
                "description": row.description if row.description else "No description available",
                "review_count": row.review_count,
                "likes": row.likes
            })

        return result
    except Exception as e:
        logger.error(f"Trending movies fetch error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching trending movies.")


# Recommened movies
@router.get("/recommended_movies/")
def get_recommended_movies(db: Session = Depends(get_db)):
    recommended = []

    # First try: genuine reviews logic
    movies = db.query(Movie).all()
    for movie in movies:
        genuine_reviews = db.query(Review).filter(
            Review.movie_id == movie.id,
            Review.prediction.ilike("%genuine%")
        ).all()

        if genuine_reviews:
            avg_rating = sum(r.rating for r in genuine_reviews) / len(genuine_reviews)
            if avg_rating >= 3.5 and len(genuine_reviews) >= 3:
                recommended.append({
                    "movie_id": movie.id,
                    "title": movie.title,
                    "genre": movie.genre,
                    "avg_rating": round(avg_rating, 2),
                    "genuine_reviews": len(genuine_reviews)
                })

    # Fallback: If no genuine reviews, show top 3 rated movies (any)
    if not recommended:
        fallback_movies = db.query(Movie).limit(3).all()
        for movie in fallback_movies:
            recommended.append({
                "movie_id": movie.id,
                "title": movie.title,
                "genre": movie.genre,
                "avg_rating": 4.0,  # Assume a decent default
                "genuine_reviews": 0
            })

    return recommended



# ✅ Get Individual Movie Details and Its Reviews
@router.get("/movies/{movie_id}/")
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    # 1. Fetch the movie
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return {"error": "Movie not found"}

    # 2. Fetch all reviews for the movie
    reviews_query = (
        db.query(Review, User.username)
        .join(User, Review.user_id == User.id)
        .filter(Review.movie_id == movie_id)
        .all()
    )

    reviews = []
    for review, username in reviews_query:
        reviews.append({
            "review_id": review.id,
            "username": username,
            "review_text": review.review_text,
            "prediction": "Fake Review" if review.prediction else "Genuine Review",
            "rating": review.rating,
            "review_date": review.review_date,
        })

    # 3. Prepare response
    movie_data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "genre": movie.genre,
        "release_year": movie.release_year,
        "reviews": reviews
    }

    return movie_data

# ✅ Add Review with Real-Time Prediction
@router.post("/add_review/")
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    try:
        # Vectorize the review text
        review_vector = vectorizer.transform([review.review_text])

        # Predict using the loaded SVM model
        prediction = svm_model.predict(review_vector)[0]  # 0 or 1

        # Save review with prediction to DB
        db_review = Review(
            movie_id=review.movie_id,
            user_id=review.user_id,
            review_text=review.review_text,
            rating=review.rating,
            review_date=review.review_date,
            prediction=prediction,
            timestamp=datetime.utcnow()
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        label = "Fake Review" if prediction else "Genuine Review"

        return {
            "message": "Review added successfully",
            "prediction": label,
            "review_id": db_review.id
        }

    except Exception as e:
        logger.error(f"Error in add_review: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Get All Reviews
# ✅ Get All Reviews with Optional Filtering
@router.get("/reviews/")
def get_reviews(
    movie_id: int = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Review, User.username, Movie.title)\
          .outerjoin(User, Review.user_id == User.id)\
          .outerjoin(Movie, Review.movie_id == Movie.id)


    if movie_id:
        query = query.filter(Review.movie_id == movie_id)
    if user_id:
        query = query.filter(Review.user_id == user_id)

    results = query.all()

    formatted_reviews = []
    for review, username, movie_title in results:
       formatted_reviews.append({
        "review_id": review.id,
        "username": username if username else "Unknown",
        "movie_title": movie_title if movie_title else "Untitled",
        "review_text": review.review_text,
        "prediction": "Fake Review" if review.prediction else "Genuine Review",
        "rating": review.rating,
        "review_date": review.review_date
    })

    print("📦 Total Reviews Fetched:", len(results))  # 🔍 Debug line
    return formatted_reviews

# 👍 Like a review
@router.post("/reviews/{review_id}/like/")
def like_review(review_id: int, user_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    existing = db.query(Like).filter(Like.user_id == user_id, Like.review_id == review_id).first()
    if existing:
        existing.is_like = True
    else:
        like = Like(user_id=user_id, review_id=review_id, is_like=True)
        db.add(like)

    db.commit()
    return {"message": "Review liked successfully."}

# 👎 Dislike a review
@router.post("/reviews/{review_id}/likes-dislikes/")
def react_to_review(review_id: int, reaction_data: ReactionCreate, db: Session = Depends(get_db)):
    user_id = reaction_data.user_id
    reaction = reaction_data.reaction  # 'like' or 'dislike'

    # Check if this user already reacted to this review
    existing = db.query(ReviewReaction).filter_by(user_id=user_id, review_id=review_id).first()

    if existing:
        # If same reaction again, remove it (toggle feature)
        if existing.reaction == reaction:
            db.delete(existing)
            db.commit()
            return {"message": f"{reaction.capitalize()} removed"}
        else:
            # Update reaction from like → dislike or vice versa
            existing.reaction = reaction
            db.commit()
            return {"message": f"Reaction updated to {reaction}"}
    else:
        # New reaction
        new_reaction = ReviewReaction(user_id=user_id, review_id=review_id, reaction=reaction)
        db.add(new_reaction)
        db.commit()
        return {"message": f"{reaction.capitalize()} added"}


#get like dislike
@router.get("/reviews/{review_id}/likes-dislikes/")
def get_likes_dislikes(review_id: int, db: Session = Depends(get_db)):
    likes = db.query(func.count()).select_from(Like).filter(
        Like.review_id == review_id, Like.is_like == True
    ).scalar()

    dislikes = db.query(func.count()).select_from(Like).filter(
        Like.review_id == review_id, Like.is_like == False
    ).scalar()

    return {
        "review_id": review_id,
        "likes": likes,
        "dislikes": dislikes
    }

# 👎 Dislike or Like a review 
@router.post("/reviews/{review_id}/likes-dislikes/")
def react_to_review(review_id: int, reaction_data: ReactionCreate, db: Session = Depends(get_db)):
    user_id = reaction_data.user_id
    reaction = reaction_data.reaction  # 'like' or 'dislike'

    existing = db.query(Like).filter_by(user_id=user_id, review_id=review_id).first()

    if existing:
        if existing.reaction == reaction:
            db.delete(existing)
            db.commit()
            return {"message": f"{reaction.capitalize()} removed"}
        else:
            existing.reaction = reaction
            db.commit()
            return {"message": f"Reaction updated to {reaction}"}
    else:
        new_reaction = Like(user_id=user_id, review_id=review_id, reaction=reaction)
        db.add(new_reaction)
        db.commit()
        return {"message": f"{reaction.capitalize()} added"}


@router.get("/users/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Count user reviews and total likes/dislikes they've given
        total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
        total_likes = db.query(Review).filter(Review.user_id == user_id, Review.likes > 0).count()
        total_dislikes = db.query(Review).filter(Review.user_id == user_id, Review.dislikes > 0).count()

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email if hasattr(user, "email") else None,
            "total_reviews": total_reviews,
            "likes_given": total_likes,
            "dislikes_given": total_dislikes
        }
    except Exception as e:
        logger.error(f"Profile fetch error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching profile")


# ✅ Predict Review 
@router.post("/predict_review/", response_model=PredictionResponse)
def predict_review(review: ReviewText):
    try:
        print("Received review:", review.review_text)
        transformed_review = vectorizer.transform([review.review_text])
        print("Vectorized shape:", transformed_review.shape)

        prediction = svm_model.predict(transformed_review)[0]
        print("Prediction result:", prediction)

        return {"prediction": "genuine" if prediction == 1 else "fake"}  

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during prediction.")





# ✅ Optional route info
@router.get("/routes-info/")
def route_info():
    return {"info": "All routes from routes.py are active"}

# Delete a review
@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}


#Search movies by partial title
@router.get("/movies/search/")
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
    if not movies:
        return {"message": "No matching movies found"}
    return movies

