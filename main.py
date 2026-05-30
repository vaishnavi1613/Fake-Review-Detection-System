from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import logging

from routes import router as api_router
from database import Base, engine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include routes from routes.py
app.include_router(api_router)

# Auto-create DB tables
Base.metadata.create_all(bind=engine)

# Load the ML model and vectorizer at startup
try:
    svm_model = joblib.load("svm_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    logger.info("✅ Model pipeline loaded successfully.")
except Exception as e:
    logger.error(f"❌ Error loading model/vectorizer: {e}")
    raise

# Input format for prediction at /predict/
class ReviewInput(BaseModel):
    review: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "🚀 Fake Review Detection API is up and running!"}


svm_model = joblib.load("svm_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

logger.info(f"Model type: {type(svm_model)}")
