import joblib

try:
    # Try loading the SVM model
    svm_model = joblib.load("svm_model.pkl")
    print("✅ SVM model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading SVM model: {e}")

try:
    # Try loading the Vectorizer
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Vectorizer loaded successfully!")
except Exception as e:
    print(f"❌ Error loading Vectorizer: {e}")
