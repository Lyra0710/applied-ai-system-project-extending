# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version (EchoMatch 1.0) loads a 20-song catalog from `data/songs.csv` and scores each song against a user's stated genre, mood, energy, and acoustic preferences using a simple additive point system (see [How The System Works](#how-the-system-works) below). It ranks songs by total score, returns the top matches with a plain-language explanation for each, and was stress-tested across 5 user profiles — including two adversarial profiles designed to surface bias in the scoring logic. See [`model_card.md`](model_card.md) for the full write-up of strengths, limitations, and experiments.

---

## How The System Works

Real world-recommendation systems like the ones in Spotify, Amazon, Netflix,
use a combination of a user's personal listening/viewing/purchase history, song/movie/product features, combined with information about other users' behavior to make personalized recommendations.
<br>
For example, if a user listens to a lot of rock music, the recommender system will recommend songs that are similar to the ones they have listened to in the past. 
If a user likes a certain type of movie, the recommender system will recommend movies that are similar to the ones they have watched in the past.
<br>
This project is a simplified version of a real-world recommendation system. It uses a simple scoring rule to make recommendations, but it does not use any machine learning or artificial intelligence. 


- What features does each `Song` use in your system
  - The features included in the dataset are id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.
  - The scoring system itself only uses `genre`, `mood`, `energy`, and `acousticness` to recommend a song (tempo, valence, and danceability are loaded but not scored).
  - The points each match is worth are:
    - mood match = +3.0
    - genre match = +1.0
    - energy match = up to +2.0 (scaled by how close the song's energy is to the user's target)
    - acoustic match = +1.0 (only if the user likes acoustic songs and the song's acousticness is 0.5 or higher)
  - These are additive, plain point values, not weights in a normalized formula — a song's final score is just the sum of whichever of these it earns.

- What information does your `UserProfile` store
  - The user profile stores the user's favorite genre, favorite mood, desired energy level, and whether they like acoustic songs.

- How does your `Recommender` compute a score for each song
  - For each song, `score_song` evaluates each rule independently and adds points when the rule is satisfied:
    - Genre and mood are categorical matches: the song's genre/mood either matches the user's favorite exactly (case-insensitive) and earns the full point value, or does not match and earns nothing.
    - Energy is a numeric similarity: the closer the song's energy is to the user's target, the more of the (up to +2.0) points it earns, using `1 - |song_energy - target_energy|` as the closeness measure.
    - Acousticness is a threshold bonus: if the user likes acoustic songs and the song's acousticness score is at least 0.5, it earns a flat +1.0.
  - No normalization step is applied — scores are the sum of these point values, so totals vary by profile depending on how many rules a song satisfies.

- How do you choose which songs to recommend
  - The recommender ranks all candidate songs by their raw score in descending order and returns the top $k$ tracks (where $k$ is requested by the user, defaulting to 5).
  - If there are fewer than $k$ songs in the catalog, it returns all scored songs.

- Potential Biases & Limitations
  - Because `mood` is a flat +3.0 bonus while `energy` is a capped continuous score (max +2.0), a strong mood match can outweigh a completely wrong energy level — so a user's stated energy preference can get overridden any time a mellow, low-energy song happens to match their mood. We confirmed this with an experiment (see below): even after doubling energy's weight relative to genre, the top-5 recommendations for every test profile came back identical, because mood's flat bonus still dominated.

<br>
### Song Features
    id
    title
    artist
    genre
    mood
    energy
    tempo_bpm
    valence
    danceability
    acousticness
<br>
### UserProfile Features
    favorite_genre
    favorite_mood
    target_energy
    likes_acoustic
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

Note: these scores reflect the current weighting after an experiment where we doubled the energy weight and halved the genre weight (genre match = +1.0, energy match = up to +2.0). See "Experiments You Tried" below.

```text
Loaded songs: 20

Profile: High-Energy Pop
Preferences: genre=pop, mood=happy, energy=0.9, likes_acoustic=False
=================================================================
Top Recommendations:

  1. Sunrise City by Neon Echo (Score: 5.84)
     Genre: pop | Mood: happy | Energy: 0.82
     Reasons: genre match (+1.0), mood match (+3.0), energy match (+1.84)

  2. Rooftop Lights by Indigo Parade (Score: 4.72)
     Genre: indie pop | Mood: happy | Energy: 0.76
     Reasons: mood match (+3.0), energy match (+1.72)

  3. Gym Hero by Max Pulse (Score: 2.94)
     Genre: pop | Mood: intense | Energy: 0.93
     Reasons: genre match (+1.0), energy match (+1.94)

  4. Storm Runner by Voltline (Score: 1.98)
     Genre: rock | Mood: intense | Energy: 0.91
     Reasons: energy match (+1.98)

  5. Neon Neon by Glitch Wizard (Score: 1.96)
     Genre: edm | Mood: euphoric | Energy: 0.88
     Reasons: energy match (+1.96)

=================================================================

Profile: Chill Lofi
Preferences: genre=lofi, mood=chill, energy=0.3, likes_acoustic=True
=================================================================
Top Recommendations:

  1. Library Rain by Paper Lanterns (Score: 6.90)
     Genre: lofi | Mood: chill | Energy: 0.35
     Reasons: genre match (+1.0), mood match (+3.0), energy match (+1.90), acoustic match (+1.0)

  2. Midnight Coding by LoRoom (Score: 6.76)
     Genre: lofi | Mood: chill | Energy: 0.42
     Reasons: genre match (+1.0), mood match (+3.0), energy match (+1.76), acoustic match (+1.0)

  3. Spacewalk Thoughts by Orbit Bloom (Score: 5.96)
     Genre: ambient | Mood: chill | Energy: 0.28
     Reasons: mood match (+3.0), energy match (+1.96), acoustic match (+1.0)

  4. Focus Flow by LoRoom (Score: 3.80)
     Genre: lofi | Mood: focused | Energy: 0.4
     Reasons: genre match (+1.0), energy match (+1.80), acoustic match (+1.0)

  5. Symphony of Hope by Vienna Strings (Score: 2.90)
     Genre: classical | Mood: peaceful | Energy: 0.25
     Reasons: energy match (+1.90), acoustic match (+1.0)

=================================================================

Profile: Deep Intense Rock
Preferences: genre=rock, mood=intense, energy=0.95, likes_acoustic=False
=================================================================
Top Recommendations:

  1. Storm Runner by Voltline (Score: 5.92)
     Genre: rock | Mood: intense | Energy: 0.91
     Reasons: genre match (+1.0), mood match (+3.0), energy match (+1.92)

  2. Gym Hero by Max Pulse (Score: 4.96)
     Genre: pop | Mood: intense | Energy: 0.93
     Reasons: mood match (+3.0), energy match (+1.96)

  3. Iron Fury by Thunderstrike (Score: 2.00)
     Genre: metal | Mood: aggressive | Energy: 0.95
     Reasons: energy match (+2.00)

  4. Neon Neon by Glitch Wizard (Score: 1.86)
     Genre: edm | Mood: euphoric | Energy: 0.88
     Reasons: energy match (+1.86)

  5. Ritmo del Sol by Salsa Caliente (Score: 1.80)
     Genre: latin | Mood: passionate | Energy: 0.85
     Reasons: energy match (+1.80)

=================================================================

Profile: Adversarial: Conflicting High-Energy Melancholic
Preferences: genre=rock, mood=melancholic, energy=0.9, likes_acoustic=True
=================================================================
Top Recommendations:

  1. Midnight Train Blues by Blind River (Score: 5.04)
     Genre: blues | Mood: melancholic | Energy: 0.42
     Reasons: mood match (+3.0), energy match (+1.04), acoustic match (+1.0)

  2. Storm Runner by Voltline (Score: 2.98)
     Genre: rock | Mood: intense | Energy: 0.91
     Reasons: genre match (+1.0), energy match (+1.98)

  3. Island Breeze by Jah Roots (Score: 2.30)
     Genre: reggae | Mood: laidback | Energy: 0.55
     Reasons: energy match (+1.30), acoustic match (+1.0)

  4. Dusty Road by Cactus Jack (Score: 2.20)
     Genre: country | Mood: nostalgic | Energy: 0.5
     Reasons: energy match (+1.20), acoustic match (+1.0)

  5. Midnight Coding by LoRoom (Score: 2.04)
     Genre: lofi | Mood: chill | Energy: 0.42
     Reasons: energy match (+1.04), acoustic match (+1.0)

=================================================================

Profile: Adversarial: Unmatched Genre with Conflicting Mood/Energy
Preferences: genre=k-pop, mood=peaceful, energy=0.95, likes_acoustic=False
=================================================================
Top Recommendations:

  1. Symphony of Hope by Vienna Strings (Score: 3.60)
     Genre: classical | Mood: peaceful | Energy: 0.25
     Reasons: mood match (+3.0), energy match (+0.60)

  2. Iron Fury by Thunderstrike (Score: 2.00)
     Genre: metal | Mood: aggressive | Energy: 0.95
     Reasons: energy match (+2.00)

  3. Gym Hero by Max Pulse (Score: 1.96)
     Genre: pop | Mood: intense | Energy: 0.93
     Reasons: energy match (+1.96)

  4. Storm Runner by Voltline (Score: 1.92)
     Genre: rock | Mood: intense | Energy: 0.91
     Reasons: energy match (+1.92)

  5. Neon Neon by Glitch Wizard (Score: 1.86)
     Genre: edm | Mood: euphoric | Energy: 0.88
     Reasons: energy match (+1.86)

=================================================================
```

---

## Experiments You Tried

We stress-tested the recommender system across 5 distinct user profiles, including 3 standard taste profiles and 2 adversarial/edge case profiles to evaluate scoring behavior under conflicting inputs:

1. **Standard Profiles ("High-Energy Pop", "Chill Lofi", "Deep Intense Rock")**:
   - The recommender successfully aligned top songs across all specified dimensions (genre, mood, energy, and acoustic preferences).
   - Songs matching both categorical metadata (`mood` +3.0 and `genre` +1.0) consistently took the top spots.

2. **Adversarial Profile 1 (Conflicting High-Energy Melancholic)**:
   - *User input*: `genre: rock`, `mood: melancholic`, `energy: 0.9`, `likes_acoustic: True`.
   - *Behavior*: The top recommended song was a slow blues track (`Midnight Train Blues`, energy 0.42, score 5.04) rather than high energy rock.
   - *Analysis*: Because `mood` match (+3.0) + `acoustic` match (+1.0) total 4.0 points, they overpower `genre` (+1.0) and numerical `energy` similarity (max 2.0). The system favors mood and acousticness over target energy.

3. **Adversarial Profile 2 (Unmatched Genre & Conflicting Mood/Energy)**:
   - *User input*: `genre: k-pop` (not in dataset), `mood: peaceful`, `energy: 0.95`.
   - *Behavior*: `Symphony of Hope` (classical, energy 0.25) ranked #1 with score 3.60 solely due to the +3.0 mood match. High energy metal/rock songs scored only ~2.00 (from energy match alone).
   - *Analysis*: Categorical mood matches dominate numeric continuous attributes like energy. Without a genre match, mood completely dictates the top recommendation even when target energy is heavily contradictory.

4. **Weight Shift Experiment (energy doubled, genre halved)**:
   - *Change*: `genre_weight` 2.0 → 1.0, and `energy_weight` scaled ×2 (so a perfect energy match is worth +2.0 instead of +1.0).
   - *Behavior*: Every song's score changed (energy-heavy songs gained up to +1.0, pure genre matches lost 1.0), but the top-5 **rankings were identical, position for position, across all 5 profiles** — confirmed by diffing the full terminal output before and after the change.
   - *Analysis*: This result was unexpected — energy was expected to begin outweighing genre for some songs. Instead, it demonstrated that the rankings are dominated by whichever song matches `mood` (+3.0, unchanged), since that value remains larger than either genre or energy alone. The recommendations became numerically different but not differently ranked, indicating this change produced different output rather than more accurate output.

---

## Limitations and Risks

- The catalog is small (20 songs), and most genres are represented by only one song, which limits how much genuine personalization the system can offer.
- The system has no understanding of lyrics, language, cultural context, or listening history — it only reasons about the four attributes it scores (genre, mood, energy, acousticness).
- Mood match is a fixed, all-or-nothing bonus (+3.0) that structurally outweighs energy (capped at +2.0) and genre (+1.0), so a user's stated energy preference can be overridden whenever a mellow, low-energy song happens to match their mood. Doubling the energy weight in an experiment did not fix this, since mood's fixed bonus remained dominant regardless of the other weights.

A deeper analysis of this bias, including specific examples, is provided in [`model_card.md`](model_card.md#6-limitations-and-bias).

---

## Reflection

Read the full write-up in [`model_card.md`](model_card.md).

Building this project clarified how directly a recommender's output is shaped by the arithmetic of its scoring rule rather than by any real understanding of music: EchoMatch turns a handful of stated preferences into point values, adds them up, and sorts the result — and that simple mechanism was enough to produce recommendations that generally felt reasonable. It also made bias easy to see once the right test cases were used: the adversarial profiles in this project showed that a feature (mood) with a disproportionately large, fixed point value can silently override a user's other stated preferences, and that this kind of bias survives reweighting other features because it is structural, not just a matter of tuning. The full experiment behind this finding is documented in [Section 6 (Limitations and Bias)](model_card.md#6-limitations-and-bias) and [Section 9 (Personal Reflection)](model_card.md#9-personal-reflection) of the model card.



