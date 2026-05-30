from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Movie Schemas
class MovieCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    category: Optional[str] = None
    price: Optional[float] = None
    description: str

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    release_year: int
    category: Optional[str]
    price: Optional[float]  
    description: str

    class Config:
        from_attributes = True  # For Pydantic v2

# Review Schemas
class ReviewCreate(BaseModel):
    user_id: int  # Replace with logged-in user's ID later
    movie_id: int
    review_text: str
    rating: Optional[int] = 5  # Optional
    review_date: Optional[datetime] = datetime.now()  # Optional

class ReviewResponse(BaseModel):
    id: int
    username: str
    movie_title: str
    review_text: str
    rating: int
    prediction: str
    review_date: datetime

    class Config:
        from_attributes = True  # to return ORM objects directly

# Prediction Schema
class ReviewText(BaseModel):
    review_text: str

# Output Schema (optional but clean)
class PredictionResponse(BaseModel):
      prediction: str  

#Rating Schema
class MovieRatingResponse(BaseModel):
    movie_id: int
    title: str
    average_rating: float
    total_reviews: int

#like/dislike

class ReactionCreate(BaseModel):
    user_id: int
    reaction: str  # should be "like" or "dislike"

