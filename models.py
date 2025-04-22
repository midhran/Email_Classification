import pandas as pd
import joblib
import os
import zipfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = "email_classifier_model.pkl"
VEC_PATH = "tfidf_vectorizer.pkl"
LBL_PATH = "label_encoder.pkl"
ZIP_PATH = "combined_emails_with_natural_pii.zip"
EXTRACT_DIR = "data"
CSV_FILE = "combined_emails_with_natural_pii.csv"

def extract_zip(zip_path=ZIP_PATH, extract_to=EXTRACT_DIR):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def train_classifier(
    save_model=True,
    model_type="logistic"
):
    # Extract the zip file containing the CSV
    extract_zip()

    csv_path = os.path.join(EXTRACT_DIR, CSV_FILE)
    df = pd.read_csv(csv_path)
    emails = df["email"]
    labels = df["type"]

    X_train, X_test, y_train, y_test = train_test_split(
        emails, labels, test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)

    model = LogisticRegression(max_iter=300)
    calibrated_model = CalibratedClassifierCV(model)
    calibrated_model.fit(X_train_vec, y_train_enc)

    preds = calibrated_model.predict(X_test_vec)
    print("\n--- Classification Report ---")
    print(classification_report(y_test_enc, preds, target_names=label_encoder.classes_))

    if save_model:
        joblib.dump(calibrated_model, MODEL_PATH)
        joblib.dump(vectorizer, VEC_PATH)
        joblib.dump(label_encoder, LBL_PATH)

    return calibrated_model, vectorizer, label_encoder

def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Training model...")
        return train_classifier()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    label_encoder = joblib.load(LBL_PATH)
    return model, vectorizer, label_encoder

def predict_category(email_text):
    model, vectorizer, label_encoder = load_model()
    vec = vectorizer.transform([email_text])
    probs = model.predict_proba(vec)[0]
    pred_idx = probs.argmax()
    label = label_encoder.inverse_transform([pred_idx])[0]
    confidence = float(round(probs[pred_idx], 4))
    return label, confidence
