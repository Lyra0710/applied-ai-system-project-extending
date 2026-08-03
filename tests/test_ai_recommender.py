import pytest
import os
from src.recommender import Song, AIRecommender

def make_test_songs():
    return [
        Song(
            id=1,
            title="Sunrise City",
            artist="Neon Echo",
            genre="pop",
            mood="happy",
            energy=0.82,
            tempo_bpm=118,
            valence=0.84,
            danceability=0.79,
            acousticness=0.18
        ),
        Song(
            id=2,
            title="Midnight Coding",
            artist="LoRoom",
            genre="lofi",
            mood="chill",
            energy=0.42,
            tempo_bpm=78,
            valence=0.56,
            danceability=0.62,
            acousticness=0.71
        )
    ]

def test_ai_recommender_fallback_mode():
    # If API key is not present, recommender should correctly use local fallback
    songs = make_test_songs()
    recommender = AIRecommender(songs, api_key=None)
    
    assert not recommender.is_api_available()
    
    # It should not fail when calling recommend, but use fallback logic
    recs, logs = recommender.recommend("Chill lofi loop", k=1)
    
    assert len(recs) == 1
    assert recs[0][0].id == 2  # Should recommend Midnight Coding
    
    # Fallback log should be present
    has_fallback_log = any("Fallback" in log["status"] for log in logs)
    assert has_fallback_log

def test_input_guardrail_fallback():
    songs = make_test_songs()
    recommender = AIRecommender(songs, api_key=None)
    
    # Query too short should get blocked
    is_safe, reason = recommender.run_input_guardrail("a")
    assert not is_safe
    assert "too short" in reason.lower()

    # Query normal should pass
    is_safe, reason = recommender.run_input_guardrail("some nice music")
    assert is_safe
