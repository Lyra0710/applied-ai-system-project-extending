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

    profiles = [
        {
            "profile_name": "High-Energy Pop",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
        },
        {
            "profile_name": "Chill Lofi",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.3,
            "likes_acoustic": True,
        },
        {
            "profile_name": "Deep Intense Rock",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
        },
        {
            "profile_name": "Adversarial: Conflicting High-Energy Melancholic",
            "genre": "rock",
            "mood": "melancholic",
            "energy": 0.9,
            "likes_acoustic": True,
        },
        {
            "profile_name": "Adversarial: Unmatched Genre with Conflicting Mood/Energy",
            "genre": "k-pop",
            "mood": "peaceful",
            "energy": 0.95,
            "likes_acoustic": False,
        },
    ]

    for user_prefs in profiles:
        name = user_prefs.get("profile_name", "User Profile")
        genre = user_prefs.get("genre", "N/A")
        mood = user_prefs.get("mood", "N/A")
        energy = user_prefs.get("energy", "N/A")
        likes_acoustic = user_prefs.get("likes_acoustic", False)

        print(f"\nProfile: {name}")
        print(f"Preferences: genre={genre}, mood={mood}, energy={energy}, likes_acoustic={likes_acoustic}")
        print("=" * 65)

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("Top Recommendations:\n")
        for idx, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"  {idx}. {song['title']} by {song['artist']} (Score: {score:.2f})")
            print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
            print(f"     Reasons: {explanation}")
            print()
        print("=" * 65)


if __name__ == "__main__":
    main()

