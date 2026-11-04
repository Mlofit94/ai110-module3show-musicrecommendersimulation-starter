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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default profile: pop / happy
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_acousticness": 0.20,
        "target_valence": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * WIDTH)
    print(f"TOP {len(recommendations)} RECOMMENDATIONS")
    print(f"Profile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}")
    print("=" * WIDTH)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
    print("\n" + "=" * WIDTH)


if __name__ == "__main__":
    main()
