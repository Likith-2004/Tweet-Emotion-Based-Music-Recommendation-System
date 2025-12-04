from flask import Flask, render_template, request, jsonify
from inference import predict_emotion
from spotify_client import recommend_songs_by_emotion
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles AJAX POST requests for emotion detection and song recommendation.
    Returns JSON (not HTML) so frontend JS can update results dynamically.
    """
    try:
        data = request.get_json() 
        tweet = data.get("tweet", "").strip()

        if not tweet:
            return jsonify({"error": "Please enter some text to analyze."}), 400

        prediction_result = predict_emotion(tweet)
        emotion = prediction_result["emotion"]
        confidence = float(prediction_result["confidence"])

        songs = recommend_songs_by_emotion(emotion)

        formatted_songs = [
            {
                "title": str(song.get("title", "")),
                "artist": str(song.get("artist", "")),
                "genre": str(song.get("genre", "")),
                "spotify_url": str(song.get("spotify_url", "")),
            }
            for song in songs
        ]

        return jsonify({
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "songs": formatted_songs
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)