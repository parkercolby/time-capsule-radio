from transformers import pipeline
import pandas as pd
from collections import defaultdict
import random
from yt_dlp import YoutubeDL  # <-- Added import for YouTube search

# Mood classification logic (unchanged)
def classify_mood(valence, energy, danceability):
    if valence > 0.75 and energy > 0.75 and danceability > 0.75:
        return "ecstatic"
    elif valence > 0.7 and energy > 0.6 and danceability > 0.6:
        return "joyful"
    elif valence > 0.6 and energy < 0.5 and danceability < 0.5:
        return "peaceful"
    elif valence < 0.3 and energy < 0.3 and danceability < 0.3:
        return "depressed"
    elif valence < 0.3 and energy > 0.7 and danceability < 0.4:
        return "angry"
    elif 0.5 < valence < 0.7 and energy > 0.7:
        return "excited"
    elif 0.4 < valence < 0.6 and energy < 0.4 and danceability < 0.5:
        return "nostalgic"
    elif valence < 0.4 and 0.5 < danceability < 0.8 and energy < 0.5:
        return "melancholy"
    elif valence > 0.7 and 0.5 < energy < 0.7 and danceability > 0.6:
        return "romantic"
    elif valence > 0.5 and energy > 0.7 and danceability < 0.4:
        return "triumphant"
    elif valence < 0.4 and energy > 0.4 and danceability > 0.7:
        return "rebellious"
    elif valence > 0.6 and energy < 0.4 and danceability > 0.6:
        return "chill"
    elif 0.3 < valence < 0.5 and 0.3 < energy < 0.5 and 0.3 < danceability < 0.5:
        return "contemplative"
    elif valence < 0.3 and energy < 0.6 and danceability > 0.7:
        return "bittersweet"
    elif valence > 0.5 and energy > 0.6 and 0.4 < danceability < 0.6:
        return "hopeful"
    else:
        return "neutral"


# Load dataset
df = pd.read_csv('dataset.csv/dataset.csv')

# Classify mood for each song
df["mood"] = df.apply(lambda row: classify_mood(row["valence"], row["energy"], row["danceability"]), axis=1)

# Map mood → list of (song, artist, popularity, explicit)
mood_to_songs = defaultdict(list)
for _, row in df.iterrows():
    mood = row["mood"]
    song = row["track_name"]
    artist = row["artists"]
    popularity = row.get("popularity", 50)
    explicit = row.get("explicit", 0)
    if song and isinstance(song, str):
        song = song.lower().strip()
        mood_to_songs[mood].append((song, artist, popularity, explicit))
mood_to_songs = {k: list(v) for k, v in mood_to_songs.items()}

# Load classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def generate_playlist(memory, artist_filters=None, playlist_length=5, min_popularity=None, explicit_allowed=True):
    candidate_labels = [
        "ecstatic", "joyful", "peaceful", "depressed", "angry", "excited",
        "nostalgic", "melancholy", "romantic", "triumphant", "rebellious",
        "chill", "contemplative", "bittersweet", "hopeful", "neutral"
    ]
    try:
        result = classifier(memory, candidate_labels)
        selected_mood = result["labels"][0]

        songs = mood_to_songs.get(selected_mood, [])

        # Artist filtering
        if artist_filters:
            songs = [(s, a, p, e) for s, a, p, e in songs if any(artist.lower() in a.lower() for artist in artist_filters)]

        # Popularity filtering
        if min_popularity is not None:
            songs = [(s, a, p, e) for s, a, p, e in songs if p >= min_popularity]

        # Explicit filtering
        if not explicit_allowed:
            songs = [(s, a, p, e) for s, a, p, e in songs if e == 0]

        # Shuffle and deduplicate
        random.shuffle(songs)
        seen = set()
        unique_songs = []
        for s, a, _, _ in songs:
            key = (s.lower(), a.lower())
            if key not in seen:
                seen.add(key)
                unique_songs.append((s, a))
            if len(unique_songs) == playlist_length:
                break

        return selected_mood, unique_songs

    except Exception as e:
        print(f"Error generating playlist: {e}")
        return None, []


# --- YouTube helper functions ---

def get_youtube_id(query):
    try:
        ydl_opts = {
            'quiet': True,
            'default_search': 'ytsearch',
            'skip_download': True,
            'format': 'bestaudio/best'
        }
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            video = result['entries'][0]
            return video['id']
    except Exception as e:
        print(f"Error fetching YouTube ID for {query}: {e}")
        return None


def build_youtube_playlist_link(video_ids):
    valid_ids = [vid for vid in video_ids if vid]
    if not valid_ids:
        return None
    return f"https://www.youtube.com/watch_videos?video_ids={','.join(valid_ids)}"
