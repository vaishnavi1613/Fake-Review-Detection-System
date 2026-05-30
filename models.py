from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    join_date = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="user")
    reviews = relationship("Review", back_populates="user")

# Movie model
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String, nullable=False)
    release_year = Column(Integer)
    description = Column(String)
    category = Column(String, nullable=True)  # New
    price = Column(Float, nullable=True)  # New

    reviews = relationship("Review", back_populates="movie")

# Review model
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    review_text = Column(String)
    prediction = Column(Integer)
    rating = Column(Float, nullable=True)  
    review_date = Column(DateTime, default=datetime.utcnow)  
    timestamp = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)         
    dislikes = Column(Integer, default=0)

    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

#like /dislike
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))
    reaction = Column(String)  # "like" or "dislike"
    is_like = Column(Boolean)  

    user = relationship("User")
    review = relationship("Review")    

class ReviewReaction(Base):
    __tablename__ = "review_reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))
    reaction = Column(String)  # 'like' or 'dislike'

    user = relationship("User")
    review = relationship("Review")


