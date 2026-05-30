import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re

# 1. Load dataset
df = pd.read_csv("IMDB_Movies.csv")

# 2. Clean reviews (basic text cleaning)
def clean_text(text):
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters/numbers
    text = text.lower()  # Lowercase
    return text

df["clean_review"] = df["review"].apply(clean_text)

# 3. Vectorize the text
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X = vectorizer.fit_transform(df["clean_review"])

# 4. Labels (0 = Negative, 1 = Positive)
y = df["sentiment"]

# 5. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train SVM
svm_model = SVC(kernel="linear")
svm_model.fit(X_train, y_train)

# 7. Evaluate
y_pred = svm_model.predict(X_test)
print("\n🔍 Classification Report:\n", classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# 8. Save model and vectorizer
joblib.dump(svm_model, "svm_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\n💾 Model and vectorizer saved as 'svm_model.pkl' and 'vectorizer.pkl'")
