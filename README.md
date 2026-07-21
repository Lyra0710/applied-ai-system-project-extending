# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.<br>
Real world-recommendation systems like the ones in Spotify, Amazon, Netflix,
use a combination of a user's personal listening/viewing/purchase history, song/movie/product features, combined with information about other users' behavior to make personalized recommendations.
<br>
For example, if a user listens to a lot of rock music, the recommender system will recommend songs that are similar to the ones they have listened to in the past. 
If a user likes a certain type of movie, the recommender system will recommend movies that are similar to the ones they have watched in the past.
<br>
This project is a simplified version of a real-world recommendation system. It uses a simple scoring rule to make recommendations, but it does not use any machine learning or artificial intelligence. 


- What features does each `Song` use in your system
  - The features included in the dataset are artist,genre,mood,energy,tempo_bpm,valence,danceability and acousticness. 
  - The scoring system used in this project specifically uses genre, mood, target energy and user favorites artist to recommend a song. 
  - The weights used in this project are:
    - mood_weight = 3.0
    - genre_weight = 2.0
    - artist_weight = 1.5
    - energy_weight = 0.1
    - valence_weight = 0.1
    - tempo_weight = 0.1

- What information does your `UserProfile` store
  - The user profile stores the user's favorite artist, preferred mood, and desired energy level.
  - The user profile also includes the user's favorite genre.

- How does your `Recommender` compute a score for each song
  - First, it compares the user profile to a song's attributes, converting matches to a similarity vector:
    - Categorical matches (mood, genre, artist) score 1.0 if they match, and 0.0 otherwise.
    - Numerical attributes (energy, valence, tempo) score a value between 0.0 and 1.0 based on how close they are to the user's targets (using absolute distance: 1 - |song_val - user_pref|).
  - The recommender then computes the final raw score by taking the dot product of this similarity vector and the user's weight vector.
  - The raw score is normalized to a scale of 0 to 100 by dividing the raw score by the maximum possible score (the sum of the weights, which is 6.8) and multiplying by 100.

- How do you choose which songs to recommend
  - The recommender ranks all candidate songs by their normalized score in descending order and returns the top $k$ tracks (where $k$ is requested by the user, defaulting to 5).
  - If there are fewer than $k$ songs in the catalog, it returns all scored songs.

- Potential Biases & Limitations
  - Because `mood` (weight 3.0) and `genre` (weight 2.0) carry the heaviest weights, this system might over-prioritize exact genre/mood matches while ignoring great songs in other genres that fit the user's desired energy or tempo.

<br>
### Song Features
    genre
    mood
    artist
    energy
    valence
    tempo_bpm
    danceability
    acousticness
<br>
### UserProfile Features
    favorite_genre
    favorite_mood
    favorite_artist
    target_energy
    likes_acoustic
    target_valence
target_tempo
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```text
Loaded songs: 20

User Profile: genre=pop, mood=happy, energy=0.8
============================================================

Top Recommendations:

  1. Sunrise City by Neon Echo (Score: 5.98)
     Genre: pop | Mood: happy | Energy: 0.82
     Reasons: genre match (+2.0), mood match (+3.0), energy match (+0.98)

  2. Rooftop Lights by Indigo Parade (Score: 3.96)
     Genre: indie pop | Mood: happy | Energy: 0.76
     Reasons: mood match (+3.0), energy match (+0.96)

  3. Gym Hero by Max Pulse (Score: 2.87)
     Genre: pop | Mood: intense | Energy: 0.93
     Reasons: genre match (+2.0), energy match (+0.87)

  4. Concrete Jungle by MC Cipher (Score: 0.98)
     Genre: hip-hop | Mood: confident | Energy: 0.78
     Reasons: energy match (+0.98)

  5. Night Drive Loop by Neon Echo (Score: 0.95)
     Genre: synthwave | Mood: moody | Energy: 0.75
     Reasons: energy match (+0.95)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



