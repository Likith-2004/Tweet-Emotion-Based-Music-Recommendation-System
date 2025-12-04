import pandas as pd
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.sparse import hstack
import joblib

MODEL_PATH = "models/lgb_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"
COLUMNS_PATH = "models/model_columns.json"
EMOJI_PATH = "models/emoji.json"
TEXT_PATH = "models/text.json"

try:
    model = joblib.load(MODEL_PATH)
    tfidf_vectorizer = joblib.load(VECTORIZER_PATH)

    with open(COLUMNS_PATH, 'r') as f:
        model_columns = json.load(f)

    with open(EMOJI_PATH, 'r') as f:
        emoji_to_emotion = json.load(f)

    with open(TEXT_PATH, 'r') as f:
        keywords_to_emotion = json.load(f)

except FileNotFoundError as e:
    print("Error: Model artifacts missing:", e)
    exit()

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#','', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    stemmed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(stemmed_tokens)

def add_features(df):
    for emotion, keywords in keywords_to_emotion.items():
        df[f'keyword_{emotion}_count'] = df['text'].apply(lambda x: sum(keyword in x.lower() for keyword in keywords))

    df['emoji_emotion'] = df['text'].apply(lambda x: next((emotion for emoji, emotion in emoji_to_emotion.items() if emoji in x), 'unknown'))
    df = pd.get_dummies(df, columns=['emoji_emotion'], prefix='emoji')
    return df

def predict_emotion(text: str):
    """
    Predicts the emotion of a given text using the trained LightGBM model.
    """
    df = pd.DataFrame([text], columns=['text'])
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    df = add_features(df)
    text_features = tfidf_vectorizer.transform(df['cleaned_text'])
    
    df_features = df.drop(columns=['text', 'cleaned_text'])
    
    for col in model_columns:
        if col not in df_features.columns:
            df_features[col] = 0
            
    df_features = df_features[model_columns]

    combined_features = hstack([text_features, df_features.astype(float)])
    
    prediction = model.predict(combined_features)[0]
    probabilities = model.predict_proba(combined_features)[0]
    
    confidence = float(probabilities.max()) * 100
    
    all_scores = {label: float(score * 100) for label, score in zip(model.classes_, probabilities)}

    return {
        "emotion": prediction,
        "confidence": f"{confidence:.2f}",
        "all_scores": {k: f"{v:.2f}" for k, v in all_scores.items()}
    }

if __name__ == '__main__':
    sample_text = "I am so incredibly happy and excited about this new journey! Yay! #blessed 😊"
    result = predict_emotion(sample_text)
    print(f"Analyzing text: '{sample_text}'")
    print(f"Predicted Emotion: {result['emotion']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"All Scores: {result['all_scores']}")