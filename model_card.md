# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**EchoMatch 1.0**

---

## 2. Intended Use  

EchoMatch is a rule-based recommendation simulation that takes a small set of explicit user preferences — favorite genre, favorite mood, target energy level, and whether the user likes acoustic songs — and returns a ranked list of songs from a fixed catalog, each with a plain-language explanation of why it was selected.

It assumes the user can state their preferences directly rather than inferring them from listening history, purchase behavior, or the behavior of similar users, as real-world recommenders typically do. It also assumes a single, static preference per user; it does not model preferences that change over time or vary by context (e.g., workout vs. studying).

This project is a classroom exploration built for AI110 to demonstrate how a simple, transparent scoring rule behaves, including where it succeeds and where it produces biased or counterintuitive results. It is not intended for real users or production deployment — the catalog is only 20 songs, and the scoring logic has known structural biases documented in Section 6.

---

## 3. How the Model Works  

EchoMatch looks at four things about a song: its genre, its mood, how energetic it is, and how acoustic it sounds. It compares these to what the user asked for and hands out points for each thing that matches:

- If the song's genre matches the user's favorite genre exactly, it earns 1 point.
- If the song's mood matches the user's favorite mood exactly, it earns 3 points — mood counts for more than any other single feature.
- Energy is not an exact match — instead, the closer the song's energy level is to what the user asked for, the more points it earns, up to 2 points for a perfect match.
- If the user says they like acoustic songs and the song is acoustic enough, it earns 1 more point.

All of these points are simply added together to get the song's final score, and the songs with the highest scores are shown first. There's no hidden math or machine learning involved — every point in a song's score can be traced back to a specific, human-readable reason, which is what gets shown in the "explanation" for each recommendation.

The starter version of this project scored songs using a normalized dot-product formula (converting every match into a 0–1 similarity value, multiplying by a weight vector, and scaling the result to a 0–100 score). This version replaces that with the simpler additive point system described above, and — as an experiment — the genre and energy point values were deliberately adjusted (genre lowered from 2 points to 1, energy's maximum raised from 1 point to 2) to test whether the recommendations became more accurate or just different. That experiment is detailed in Section 7.

---

## 4. Data  

The catalog contains 20 songs, loaded from `data/songs.csv`. Each song has 9 attributes: title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness. Of these, the scoring logic actively uses genre, mood, energy, and acousticness; tempo, valence, and danceability are loaded but currently unused by the scoring function.

The catalog spans 17 different genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, metal, reggae, hip-hop, edm, country, blues, funk, folk, and latin) and 16 different moods (happy, chill, intense, relaxed, moody, focused, peaceful, aggressive, laidback, confident, euphoric, nostalgic, melancholic, groovy, reflective, and passionate). Only lofi (3 songs) and pop (2 songs) have more than one entry — every other genre is represented by exactly one song. No songs were added to or removed from the original starter dataset.

Because the catalog is small and each genre is so thinly represented, several parts of musical taste are effectively missing: there is no representation of multi-genre or fusion songs (each song has exactly one genre label), no lyrical or language information, no measure of popularity or cultural context, and no notion of a user's listening history or how their taste might evolve. With only one or two songs per genre in most cases, the recommender cannot meaningfully distinguish between "songs in this genre I'd like" and "the only song in this genre," which limits how much genuine personalization it can offer.

---

## 5. Strengths  

EchoMatch performs best for user profiles whose genre, mood, and energy preferences all point toward the same kind of song — for example, a "Chill Lofi" profile (lofi genre, chill mood, low energy, likes acoustic) correctly surfaces genuinely chill, acoustic lofi tracks at the top of its recommendations, and a "High-Energy Pop" profile correctly surfaces upbeat, high-energy pop tracks. In these non-conflicting cases, the additive scoring captures the intuitive answer: songs matching more of the user's stated preferences reliably outrank songs matching fewer.

The explanation output is also a clear strength — because every point is tied to a specific, named rule (genre match, mood match, energy match, acoustic match), the reasoning behind any recommendation is fully traceable and never a "black box," which was confirmed while manually checking recommendations against the underlying CSV data during testing.

The main limitation of this strength is that it only holds when a user's stated preferences do not conflict with one another; Section 6 and Section 7 document what happens once they do.

---

## 6. Limitations and Bias 

The scoring logic systematically overrides a user's stated energy preference whenever mood and acousticness align on a low-energy song, because a mood match (+3.0) combined with an acoustic match (+1.0) can exceed even a perfect energy score (maximum +1.0 in the original weighting). This was observed directly in Adversarial Profile 1: a user specifying `energy: 0.9` was recommended *Midnight Train Blues* (energy 0.42) as the top track, because its mood and acoustic attributes matched while its energy did not. To determine whether this could be resolved through reweighting alone, an experiment was conducted that doubled the energy weight and halved the genre weight. Even at twice the original weight, energy's maximum contribution (+2.0) remained below mood's fixed +3.0, and the top-5 rankings for all five profiles were identical to the baseline. This indicates a structural bias rather than a tuning issue: mood functions as a categorical, all-or-nothing bonus, while energy is a continuous similarity score with a lower ceiling. As a result, users whose energy requirements conflict with a strong mood or genre match (for example, someone requesting an "intense" or "high-energy" but melancholic song) are consistently directed toward calmer, lower-energy tracks regardless of how the weights are adjusted. A more complete solution would require either scaling energy's ceiling to be competitive with mood's, or representing mood itself as a continuous value (for example, via a valence/arousal space) rather than a fixed categorical bonus.

---

## 7. Evaluation  

We stress-tested the recommender system across 5 distinct user profiles defined in `src/main.py`:

- **Profiles Tested**:
  1. *High-Energy Pop*: `genre: pop`, `mood: happy`, `energy: 0.9`
  2. *Chill Lofi*: `genre: lofi`, `mood: chill`, `energy: 0.3`, `likes_acoustic: True`
  3. *Deep Intense Rock*: `genre: rock`, `mood: intense`, `energy: 0.95`
  4. *Adversarial 1 (Conflicting High-Energy Melancholic)*: `genre: rock`, `mood: melancholic`, `energy: 0.9`, `likes_acoustic: True`
  5. *Adversarial 2 (Unmatched Genre + Contradictory Mood/Energy)*: `genre: k-pop`, `mood: peaceful`, `energy: 0.95`

  (Scores below reflect the current weighting after our Step 3 experiment: genre match is worth +1.0 and energy match is worth up to +2.0, versus the original +2.0 / +1.0 split.)

- **What Surprised Us**: The two adversarial profiles were expected to produce clearly invalid or incoherent top picks. Instead, the system consistently produced a plausible-looking result at #1 — it substituted the feature the user actually specified (energy) with whichever feature it could still match (mood). The recommendations do not appear incorrect on inspection; the energy value must be checked directly to identify that the stated preference was not honored.

- **Pairwise Comparisons**:

  - **High-Energy Pop vs. Chill Lofi** — These two profiles request opposite characteristics (high-energy/upbeat vs. low-energy/acoustic), and the system distinguishes them correctly: High-Energy Pop receives an upbeat track (*Sunrise City*, energy 0.82), while Chill Lofi receives a mellow, acoustic-heavy track (*Library Rain*, energy 0.35, acousticness 0.86). This is consistent with expectations — when a user's genre, mood, and energy targets all align, the additive scoring correctly surfaces the best-matching song.

  - **High-Energy Pop vs. Deep Intense Rock** — Both profiles request high energy (0.9 and 0.95), but the system still differentiates them: Pop receives a bright, upbeat track (*Sunrise City*), while Rock receives a more intense, driving track (*Storm Runner*). This demonstrates the system working as intended — genre and mood act as a secondary filter on top of the energy level, so two high-energy profiles with different tastes still receive distinct recommendations rather than the same generic high-energy track.

  - **Deep Intense Rock vs. Adversarial 1 (Conflicting High-Energy Melancholic)** — Both profiles request rock at a comparable energy level (approximately 0.9–0.95), but Deep Intense Rock specifies an "intense" mood while Adversarial 1 specifies "melancholic." That single change in mood entirely changes the top result — from a rock track (*Storm Runner*) to a slow blues track (*Midnight Train Blues*, energy 0.42, a different genre entirely). This outcome is inconsistent with the user's stated intent: despite requesting high energy, a single mismatched mood term caused the system to disregard both the genre and energy targets in favor of the calmest track in the catalog. This is the clearest evidence that mood currently functions as the dominant factor overriding all others.

  - **Chill Lofi vs. Adversarial 1** — Both profiles specify `likes_acoustic: True`, but Chill Lofi targets low energy (0.3) while Adversarial 1 targets high energy (0.9). Despite this difference, both profiles' top picks are low-energy tracks (*Library Rain* at 0.35, *Midnight Train Blues* at 0.42) — the acoustic bonus and mood match direct both profiles toward the same low-energy segment of the catalog regardless of their stated energy targets. In effect, `likes_acoustic` is functioning as a proxy for "prefers a calm track," which is not equivalent to the user's actual request.

  - **Adversarial 2 (Unmatched Genre + Contradictory Mood/Energy)** — This profile requests a genre absent from the catalog ("k-pop"), a peaceful mood, and high energy (0.95) simultaneously — a combination unlikely to correspond well to any single track. With no genre to match, the system relies entirely on mood and returns *Symphony of Hope*, a slow classical piece at energy 0.25, which is markedly inconsistent with the requested energy level. This outcome follows directly from the scoring logic (mood is the strongest remaining factor once genre is eliminated), but it illustrates that the system will return a confident top recommendation even for a query that arguably has no good match in the catalog.

  - **Why does "Gym Hero" keep appearing for "Happy Pop" profiles?** — Consider the High-Energy Pop profile, which requests `pop` + `happy` + high energy. *Gym Hero* is `pop` + `intense` (not "happy") + energy 0.93, yet it still ranks #3. This occurs because the system does not require a song to satisfy every stated preference — it simply accumulates points for whichever attributes happen to match. *Gym Hero* earns points for genre and energy alone, and that combined total is sufficient to outrank tracks that match neither attribute, even though its mood does not match. Consequently, a fast, high-energy pop track will continue to appear in "happy pop" recommendations whenever it is sufficiently energetic, even when its actual mood is closer to an intense workout track than a cheerful pop song.

- **Terminal Output**:
  Full terminal outputs for all 5 profiles are recorded in the `README.md` under [Sample Recommendation Output](README.md#sample-recommendation-output).


---

## 8. Future Work  

The most important next step would be addressing the mood-dominance bias identified in Section 6, likely by replacing the exact-match mood bonus with a continuous mood similarity score (for example, mapping moods into a valence/arousal space so "intense" and "melancholic" are recognized as different but not maximally opposed, rather than simply "match" or "no match"). This would prevent a single mismatched mood word from completely overriding a user's stated energy and genre preferences.

Beyond that, several improvements would make the system more realistic and more useful:

- **Additional features or preferences**: incorporate tempo, valence, and danceability (currently loaded but unused) into scoring, and allow users to specify a favorite artist or an explicit "avoid" list.
- **Better explanations**: show each song's relative contribution as a percentage of its total score, so a user can see not just *that* mood mattered, but *how much* it mattered compared to genre or energy.
- **More diversity among results**: the current system always returns the exact same top 5 songs for a given profile; introducing a diversity mechanism (e.g., penalizing songs too similar to ones already recommended) would surface a wider range of the catalog.
- **Handling more complex tastes**: support multiple favorite genres or moods per user, and add a "no strong match" fallback so the system can signal when a request (like the unmatched-genre adversarial profile in Section 7) genuinely has no good answer in the catalog, rather than confidently returning its best-available guess.

---

## 9. Personal Reflection & Ethics

### Limitations or Biases in the System
EchoMatch 2.0 is constrained by the following limitations and biases:
1. **Catalog Constraints**: The in-context catalog is small (only 20 songs). When user queries specify genres or moods outside this set, the LLM must compromise or map them to close matches, which can lead to over-generalization.
2. **Mood Dominance**: The model card analysis in Section 6 shows that categorical mood matches structurally dominate numeric features (such as energy similarity). This means a user requesting intense music who mentions a sad mood is pushed toward calm tracks.
3. **Data Representation Bias**: Features like mood and genre are represented as flat, categorical strings. This ignores the reality of musical genres (which exist on a spectrum) and moods (which are multidimensional).

### AI Misuse and Prevention
1. **Misuse Potential**: Because the recommender allows free-form natural language query inputs, it could be subject to prompt injection attacks aimed at leaking developer instructions, serving as a general-purpose chat interface, or outputting inappropriate content.
2. **Prevention Strategy**: We implemented an **Input Guardrail** as a first-line check. This guardrail uses structured output to evaluate the incoming prompt's safety and music-related context *before* feeding it to the retriever or recommendation agents. If the check fails, the query is immediately rejected and execution halts safely.

### Reliability Testing Surprises
During automated and manual verification:
1. **Plausibility Illusion**: I was surprised by how coherent the system's output appeared even during adversarial profiles. When tested with unmatched parameters, the Recommender Agent generated highly convincing explanations for sub-optimal tracks. Without directly inspecting numeric attributes (like energy levels), it is easy to assume the recommendation is highly accurate when it actually represents a compromise.
2. **Guardrail Edge Cases**: Fallback modes must be tested robustly. When testing the guardrail offline (without an API key), a simple length-based heuristic fallback was required to ensure the application did not crash, indicating that hybrid local/AI systems need dual-layered validation checks.

### AI Collaboration and Suggestions
Throughout this project, I collaborated with the AI coding assistant for design, prototyping, and debugging:
1. **Helpful Suggestion**: The assistant recommended using Pydantic schemas with Gemini's structured schema output (`response_schema`). This forced the AI model to output validated JSON, resolving parsing errors and ensuring that the self-critique loop operated on predictable key-value fields.
2. **Flawed Suggestion**: The assistant initially suggested executing the Streamlit app using standard `python src/app.py` in the setup instructions. Since Streamlit pages must be served using the Streamlit execution engine, this failed, and had to be corrected to `streamlit run src/app.py`.


