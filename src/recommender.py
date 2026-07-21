import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_dict = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = song.__dict__
            score, _ = score_song(user_dict, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_dict = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }
        _, reasons = score_song(user_dict, song.__dict__)
        return ", ".join(reasons) if reasons else "No specific match"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries with type conversions."""
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']) if 'id' in row and row['id'] else 0,
                'title': row.get('title', ''),
                'artist': row.get('artist', ''),
                'genre': row.get('genre', ''),
                'mood': row.get('mood', ''),
                'energy': float(row['energy']) if 'energy' in row and row['energy'] else 0.0,
                'tempo_bpm': float(row['tempo_bpm']) if 'tempo_bpm' in row and row['tempo_bpm'] else 0.0,
                'valence': float(row['valence']) if 'valence' in row and row['valence'] else 0.0,
                'danceability': float(row['danceability']) if 'danceability' in row and row['danceability'] else 0.0,
                'acousticness': float(row['acousticness']) if 'acousticness' in row and row['acousticness'] else 0.0,
            }
            songs.append(song)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return numeric score with explanation reasons."""
    score = 0.0
    reasons = []

    # 1. Genre match (+1.0) -- half weight (experiment: weight shift toward energy)
    target_genre = user_prefs.get('genre') or user_prefs.get('favorite_genre')
    if target_genre and song.get('genre', '').lower() == target_genre.lower():
        score += 1.0
        reasons.append("genre match (+1.0)")

    # 2. Mood match (+3.0)
    target_mood = user_prefs.get('mood') or user_prefs.get('favorite_mood')
    if target_mood and song.get('mood', '').lower() == target_mood.lower():
        score += 3.0
        reasons.append("mood match (+3.0)")

    # 3. Artist match (+1.5)
    target_artist = user_prefs.get('artist') or user_prefs.get('favorite_artist')
    if target_artist and song.get('artist', '').lower() == target_artist.lower():
        score += 1.5
        reasons.append("artist match (+1.5)")

    # 4. Energy match (numerical similarity: 1 - |song_energy - target_energy|), weight x2 (experiment: weight shift toward energy)
    target_energy = user_prefs.get('energy') if 'energy' in user_prefs else user_prefs.get('target_energy')
    if target_energy is not None and 'energy' in song:
        energy_diff = abs(float(song['energy']) - float(target_energy))
        energy_sim = max(0.0, 1.0 - energy_diff)
        energy_pts = round(energy_sim * 2.0, 2)
        score += energy_pts
        reasons.append(f"energy match (+{energy_pts:.2f})")

    # 5. Acousticness preference (+1.0 point if user likes acoustic and song acousticness >= 0.5)
    if user_prefs.get('likes_acoustic'):
        if song.get('acousticness', 0.0) >= 0.5:
            score += 1.0
            reasons.append("acoustic match (+1.0)")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score using score_song and return top k recommendations with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "No specific preference match"
        scored_songs.append((song, score, explanation))

    # Return top k recommendations sorted by score (item[1]) from highest to lowest
    return sorted(scored_songs, key=lambda item: item[1], reverse=True)[:k]
