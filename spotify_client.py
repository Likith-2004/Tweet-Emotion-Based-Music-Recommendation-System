import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# The list of sub-genres for each primary emotion
EMOTION_TO_GENRE = {
    "joy": [
        "electropop", "tropical house", "indie pop", "funk", "bubblegum pop", 
        "dance-pop", "soul", "disco"
    ],
    "sadness": [
        "indie folk", "soft piano", "ambient acoustic", "slowcore", "melancholic lo-fi", 
        "singer-songwriter", "post-rock", "blues"
    ],
    "anger": [
        "hardcore punk", "nu metal", "industrial rock", "thrash metal", "grunge", 
        "metalcore", "hard rock", "trap-metal"
    ],
    "fear": [
        "dark ambient", "drone", "experimental electronic", "minimal classical", "soundscape", 
        "darksynth", "industrial", "noise"
    ],
    "love": [
        "neo-soul", "r-n-b", "soft rock", "jazz pop", "dream pop", 
        "quiet storm", "alternative-rnb", "bossa-nova"
    ],
    "surprise": [
        "glitch", "hyperpop", "experimental indie", "psychedelic electronic", "avant-garde", 
        "breakcore", "free-jazz", "math-rock"
    ]
}

def get_spotify_client():
    """Authenticate with Spotify API using OAuth2 credentials."""
    try:
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError("❌ Spotify credentials missing in .env file")

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-library-read"
            )
        )
        return sp
    except Exception as e:
        print(f"[ERROR] Spotify authentication failed: {e}")
        return None

def recommend_songs_by_emotion(emotion: str, limit: int = 5):
    """
    Recommends a diverse playlist of songs based on a list of seed genres
    for the given emotion.
    """
    sp = get_spotify_client()
    if sp:
        # Get the list of up to 5 genres for the emotion
        genres = EMOTION_TO_GENRE.get(emotion.lower())
        if not genres:
            print(f"[WARN] No genres defined for emotion: {emotion}. Using fallback.")
            return fallback_recommendations(emotion, limit)

        try:
            print(f"[INFO] Getting recommendations based on seeds: {genres}")
            results = sp.recommendations(seed_genres=genres, limit=limit)

            if not results or not results['tracks']:
                 print("[WARN] Spotify API returned no songs for the given genres. Using fallback.")
                 return fallback_recommendations(emotion, limit)

            recommended_tracks = []
            for track in results['tracks']:
                recommended_tracks.append({
                    "title": track["name"],
                    "artist": ", ".join(artist["name"] for artist in track["artists"]),
                    "spotify_url": track["external_urls"]["spotify"],
                    "album_cover_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "https://i.imgur.com/7Q7gB7p.png" # A default image
                })
            
            return recommended_tracks
        except Exception as e:
            print(f"[ERROR] Spotify API request failed: {e}")
            return fallback_recommendations(emotion, limit)
    else:
        print("[INFO] Spotify client unavailable. Using fallback songs.")
        return fallback_recommendations(emotion, limit)

def fallback_recommendations(emotion: str, limit: int = 5):
    """
    Load fallback songs from a local CSV if the Spotify API fails.
    """
    try:
        df = pd.read_csv("spotify_fallback_songs.csv")
        df['genre'] = df['genre'].str.lower()
        df_filtered = df[df['genre'] == emotion.lower()]

        if df_filtered.empty:
            print(f"[WARN] No fallback songs for '{emotion}'. Returning random picks.")
            df_filtered = df.sample(n=min(limit, len(df)))

        return df_filtered.sample(n=min(limit, len(df_filtered))).to_dict(orient="records")
    except FileNotFoundError:
        print("[ERROR] Fallback CSV 'spotify_fallback_songs.csv' not found.")
        return []
    except Exception as e:
        print(f"[ERROR] Fallback recommendation error: {e}")
        return []

if __name__ == "__main__":
    emotion_input = input("Enter detected emotion (e.g., joy, sadness): ").strip()
    songs = recommend_songs_by_emotion(emotion_input)
    
    if not songs:
        print(f"⚠️ Could not find any songs for '{emotion_input}'.")
    else:
        print(f"\n🎵 Here are some songs for the emotion '{emotion_input.capitalize()}':")
        for i, song in enumerate(songs, 1):
            print(f"  {i}. {song['title']} by {song['artist']}")
            print(f"     Listen here: {song['spotify_url']}")