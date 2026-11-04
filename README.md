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

Real-world platforms like Spotify and YouTube blend collaborative filtering (learning from what millions of listeners play, skip, and save) with content-based filtering (matching the audio traits of songs), then rank the candidates. My version has no listening history, so it is purely content-based. It compares each song's attributes to a user's stated taste and prioritizes how *close* a song is to what the user wants, not whether its values are high or low. Energy and mood matter most, followed by acousticness, valence, and genre.

**`Song` features**

- `genre`
- `mood`
- `energy`
- `acousticness`
- `valence`
- `tempo_bpm` and `danceability` (stored, but given little or no weight because they overlap with energy)

**`UserProfile` features**

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_acousticness`
- `target_valence`

**Algorithm Recipe**

1. **Input:** a user profile and the songs loaded from `data/songs.csv`.
2. **Score every song** (a number from 0 to 1) with this formula:

   ```
   score = 0.30 * (1 - |song.energy       - target_energy|)
         + 0.20 * (1 - |song.acousticness - target_acousticness|)
         + 0.15 * (1 - |song.valence      - target_valence|)
         + 0.25 * (1 if song.mood  == favorite_mood  else 0)
         + 0.10 * (1 if song.genre == favorite_genre else 0)
   ```

   Numeric features reward songs that are *close* to the target, not songs with higher or lower values. Mood is weighted above genre because mood describes the listening situation and genre is too narrow in a small catalog.
3. **Rank:** sort songs by score, highest first. Ties go to the song with the smaller energy gap. Return the top K, each with a short reason for why it was picked.

**Expected biases**

- **Filter bubble:** the system only rewards what the user already said they like, so it will never suggest anything unexpected.
- **Exact matching:** mood and genre are all-or-nothing, so "focused" counts as no match for "chill", and a metal song gets no credit for a "rock" fan even when the numbers fit.
- **Mood over genre:** a song with the right mood but the wrong genre can outrank a genre match.
- **Small catalog:** with only 18 songs, some genres and moods have a single song, so results may repeat or cluster.
- **Fixed weights:** every user is scored with the same weights, even though some listeners care more about energy and others about mood.

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

Output of `python -m src.main` for the default pop / happy profile:

```
Loaded songs: 18

================================================================
TOP 5 RECOMMENDATIONS
Profile: pop / happy
================================================================

#1  Sunrise City by Neon Echo
    Score: 0.98 / 1.00
    Reasons:
      - mood matches (happy) +0.25
      - genre matches (pop) +0.10
      - energy 0.82 vs target 0.80 +0.29
      - acousticness 0.18 vs target 0.20 +0.20
      - valence 0.84 vs target 0.80 +0.14

#2  Rooftop Lights by Indigo Parade
    Score: 0.86 / 1.00
    Reasons:
      - mood matches (happy) +0.25
      - energy 0.76 vs target 0.80 +0.29
      - acousticness 0.35 vs target 0.20 +0.17
      - valence 0.81 vs target 0.80 +0.15

#3  Gym Hero by Max Pulse
    Score: 0.68 / 1.00
    Reasons:
      - genre matches (pop) +0.10
      - energy 0.93 vs target 0.80 +0.26
      - acousticness 0.05 vs target 0.20 +0.17
      - valence 0.77 vs target 0.80 +0.15

#4  Concrete Crown by Kid Meridian
    Score: 0.60 / 1.00
    Reasons:
      - energy 0.78 vs target 0.80 +0.29
      - acousticness 0.12 vs target 0.20 +0.18
      - valence 0.62 vs target 0.80 +0.12

#5  Night Drive Loop by Neon Echo
    Score: 0.58 / 1.00
    Reasons:
      - energy 0.75 vs target 0.80 +0.28
      - acousticness 0.22 vs target 0.20 +0.20
      - valence 0.49 vs target 0.80 +0.10

================================================================
```

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



