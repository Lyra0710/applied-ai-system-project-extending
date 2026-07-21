"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print(f"\nUser Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations:\n")
    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"  {idx}. {song['title']} by {song['artist']} (Score: {score:.2f})")
        print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"     Reasons: {explanation}")
        print()
    print("=" * 60)


if __name__ == "__main__":
    main()
