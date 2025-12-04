# 🎧 Tweet-Emotion-Based-Music-Recommendation-System

An intelligent web application that detects the emotional tone of your text inputs and curates a personalized Spotify playlist to match your mood. Whether you're feeling joyful, sad, or full of rage, this app finds the perfect soundtrack for your feelings.

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Spotify API Setup Guide](#-spotify-api-setup-guide)
- [Usage](#-usage)
- [Model Training](#-model-training)
- [Troubleshooting](#-troubleshooting)

---

## 📖 About the Project
This project combines **Natural Language Processing (NLP)** with the **Spotify Web API**. It takes a user's text (a tweet, a diary entry, or just a random thought), analyzes it using a trained **LightGBM** machine learning model, and classifies it into one of six core emotions:

- Joy  
- Sadness  
- Anger  
- Fear  
- Love  
- Surprise  

Based on the detected emotion, the application connects to Spotify to fetch song recommendations from specific genres associated with that mood, displaying them with embedded players for instant listening.

---

## ✨ Features
- **Real-time Emotion Detection**: Analyzes text input instantly.  
- **Smart Music Recommendation**: Maps emotions to specific musical genres (e.g., Joy → Pop/Disco, Fear → Dark Ambient).  
- **Dynamic & Random**: Shuffles genres and selects random tracks for variety.  
- **Resilient Fetching**: Automatically switches to the next genre if Spotify returns no results.  
- **Robust Fallback**: Uses a local CSV backup dataset if the API is unreachable.  
- **Interactive UI**: Clean, responsive HTML/CSS interface with embedded Spotify players.

---

## 🛠 Tech Stack
- **Backend**: Python, Flask  
- **Machine Learning**: Scikit-Learn (TF-IDF), LightGBM, NLTK  
- **API**: Spotipy (Spotify Web API Wrapper)  
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)  
- **Data Handling**: Pandas, JSON  

---

## 📂 Project Structure
```bash
tweet-emotion-music/
│
├── data/
│   ├── emotion_examples.json          # Training examples
│   ├── emotion_support.json           # Supplemental keywords
│   ├── text.json                      # Core keywords
│   └── spotify_fallback_songs.csv     # Backup song list
│
├── models/
│   ├── lgb_model.pkl                  # Trained LightGBM Model
│   ├── tfidf_vectorizer.pkl           # TF-IDF Vectorizer
│   └── model_columns.json             # Feature column alignment
│
├── templates/
│   └── index.html                     # Frontend Interface
│
├── app.py                             # Flask Application Entry Point
├── inference.py                       # ML Prediction Logic
├── spotify_client.py                  # Spotify API & Recommendation Logic
├── train_model.py                     # Script to retrain the model
├── .env                               # API Credentials (Hidden)
└── requirements.txt                   # Python Dependencies
```

---

# 📊 Dataset

The model is trained and supported by a specific set of data files located in the `data/` directory.

## 1. Download the Data

The core training dataset is hosted on Kaggle. You can download it using one of the methods below:

**Link:** [Twitter Emotion Dataset (vklikith/tweet-dataset)](https://www.kaggle.com/datasets/vklikith/tweet-dataset)

### Option A: Direct Download (Web Interface)

1. Click the dataset link above.
2. Click the **Download** button (top right of the page).
3. Unzip the downloaded `archive.zip` file.
4. Move the following files into your project's `data/` folder:
   * `train.csv`
   * `val.csv`
   * `test.csv`

### Option B: Using Kaggle API

If you have the Kaggle API installed and configured:
```bash
kaggle datasets download -d vklikith/tweet-dataset
unzip tweet-dataset.zip -d data/
```

## 2. File Descriptions

* **Training Data** (`train.csv`, `val.csv`): A collection of tweets labeled with six core emotions: joy, sadness, anger, fear, love, and surprise.
* **Feature Engineering Resources** (`text.json`, `emotion_support.json`): Custom dictionaries mapping specific keywords, emojis, and phrases to emotions. These are used to create "keyword count" features that significantly boost model accuracy.
* **Fallback Music Database** (`spotify_fallback_songs.csv`): A curated list of songs with Spotify URLs. This ensures the application can still recommend music even if the Spotify API limit is reached or the service is down.

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8 or higher  
- A Spotify Account  

---

## **Installation**

### **1. Clone the repository:**
```bash
git clone https://github.com/yourusername/tweet-emotion-music.git
cd tweet-emotion-music
```
## 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```

### Activate the Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 2. Activate the Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Spotify API Setup Guide

To fetch live songs, you need Spotify developer credentials. Follow these steps:

### Step 1: Log in to the Developer Dashboard

Go to: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

Log in with your regular Spotify account.

### Step 2: Create an App

1. Click **Create An App**
2. **App Name:** Emotion Music Recommender
3. **Description:** Recommends music based on text emotion
4. **Redirect URI:** `http://localhost:5000/callback`
5. Check the agreement box → **Create**

### Step 3: Get Your Credentials

1. Open the app dashboard → Click **Settings**
2. Copy:
   - **Client ID**
   - **Client Secret**

### Step 4: Configure the Project

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=enter_client_ID_here
SPOTIFY_CLIENT_SECRET=enter_client_secret_here
SPOTIFY_REDIRECT_URI=enter_redirect_uri_here
```

⚠️ **Do not add quotes.**

---

## 🎮 Usage

### Run the Flask Application

```bash
python app.py
```

### Open Your Browser

Navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Interact

1. Type something describing your mood
2. Click **Detect Emotion & Recommend Songs**
3. Enjoy your personalized playlist 🎵

---

## 🧠 Model Training

If you want to retrain the model:

1. Ensure your datasets (`train.csv`, `val.csv`) are inside the `data/` directory.
2. Run the training script:

```bash
python train_model.py
```

New model artifacts will appear in the `models/` directory.

---

## 🔧 Troubleshooting

### ❌ Error: Spotify Client Authentication Failed

- Check `.env` formatting
- Ensure no trailing spaces
- Delete `.cache` and restart the app

### 🎵 No Songs Appearing

- Ensure `spotify_client.py` runs without errors
- Confirm `spotify_fallback_songs.csv` exists and contains data

### 🌐 Browser Error: BadRequestKeyError

- Clear your cache (`Ctrl + Shift + R`)
