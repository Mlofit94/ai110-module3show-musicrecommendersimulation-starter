"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs  # python src/main.py

WIDTH = 64


# Three distinct, realistic taste profiles.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "target_acousticness": 0.10,
        "target_valence": 0.85,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_acousticness": 0.80,
        "target_valence": 0.58,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_acousticness": 0.08,
        "target_valence": 0.40,
    },
}

# Adversarial / edge-case profiles meant to trick the scoring logic.
ADVERSARIAL_PROFILES = {
    "Conflict: high energy + sad mood": {
        # No song has mood "sad", so the 0.25 mood bonus can never fire.
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_acousticness": 0.10,
        "target_valence": 0.10,
    },
    "Conflict: angry mood + acoustic + calm": {
        # Mood wants metal-like songs; numeric targets want quiet acoustic ones.
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.10,
        "target_acousticness": 0.95,
        "target_valence": 0.90,
    },
    "Unknown genre and mood": {
        # Neither categorical feature can match; only numerics decide.
        "favorite_genre": "k-pop",
        "favorite_mood": "dreamy",
        "target_energy": 0.50,
        "target_acousticness": 0.50,
        "target_valence": 0.50,
    },
    "Case/whitespace mismatch": {
        # Exact string matching misses "Pop " vs "pop".
        "favorite_genre": "Pop ",
        "favorite_mood": "Happy",
        "target_energy": 0.80,
        "target_acousticness": 0.20,
        "target_valence": 0.80,
    },
    "Out-of-range targets": {
        # Targets outside 0..1 push per-feature points negative.
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 1.80,
        "target_acousticness": -0.50,
        "target_valence": 1.50,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * WIDTH)
    print(f"{name.upper()} - TOP {len(recommendations)}")
    print(f"Profile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}")
    print("=" * WIDTH)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in {**PROFILES, **ADVERSARIAL_PROFILES}.items():
        print_recommendations(name, prefs, songs)
    print("\n" + "=" * WIDTH)


if __name__ == "__main__":
    main()
