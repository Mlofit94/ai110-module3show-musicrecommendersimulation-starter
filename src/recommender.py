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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into dicts, converting id to int and numeric columns to float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

# EXPERIMENT (weight shift): energy doubled (0.30 -> 0.60) and genre halved
# (0.10 -> 0.05). Raw weights now sum to 1.25, so each is divided by 1.25 to
# keep the total score within 0 to 1. Revert with `git checkout src/recommender.py`.
_RAW_WEIGHTS = {"mood": 0.25, "genre": 0.05, "energy": 0.60, "acousticness": 0.20, "valence": 0.15}
_TOTAL = sum(_RAW_WEIGHTS.values())
MOOD_POINTS = _RAW_WEIGHTS["mood"] / _TOTAL
GENRE_POINTS = _RAW_WEIGHTS["genre"] / _TOTAL
NUMERIC_FEATURES = [
    # (song field, user_prefs key, weight)
    ("energy", "target_energy", _RAW_WEIGHTS["energy"] / _TOTAL),
    ("acousticness", "target_acousticness", _RAW_WEIGHTS["acousticness"] / _TOTAL),
    ("valence", "target_valence", _RAW_WEIGHTS["valence"] / _TOTAL),
]
assert abs(MOOD_POINTS + GENRE_POINTS + sum(w for _, _, w in NUMERIC_FEATURES) - 1.0) < 1e-9

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song from 0 to 1 against a user profile and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Categorical features: all-or-nothing bonus for an exact match.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood matches ({song['mood']}) +{MOOD_POINTS:.2f}")
    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre matches ({song['genre']}) +{GENRE_POINTS:.2f}")

    # Numeric features: full points at the target, fewer the further away.
    for feature, target_key, weight in NUMERIC_FEATURES:
        target = user_prefs[target_key]
        points = weight * (1 - abs(song[feature] - target))
        score += points
        reasons.append(
            f"{feature} {song[feature]:.2f} vs target {target:.2f} +{points:.2f}"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    # Judge every song with score_song, then sort best-first. Ties go to the
    # smaller energy gap, then the lower id.
    ranked = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: (
            -item[1],
            abs(item[0]["energy"] - user_prefs["target_energy"]),
            item[0]["id"],
        ),
    )
    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in ranked[:k]
    ]
