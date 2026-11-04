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

## Sample Output by Profile

Terminal output from `python src/main.py` for each profile (first three are normal profiles, the rest are adversarial edge cases).

### High-Energy Pop

```text
================================================================
HIGH-ENERGY POP - TOP 5
Profile: pop / happy
================================================================

#1  Sunrise City by Neon Echo
    Score: 0.96 / 1.00
    Reasons:
      - mood matches (happy) +0.25
      - genre matches (pop) +0.10
      - energy 0.82 vs target 0.90 +0.28
      - acousticness 0.18 vs target 0.10 +0.18
      - valence 0.84 vs target 0.85 +0.15

#2  Rooftop Lights by Indigo Parade
    Score: 0.80 / 1.00
    Reasons:
      - mood matches (happy) +0.25
      - energy 0.76 vs target 0.90 +0.26
      - acousticness 0.35 vs target 0.10 +0.15
      - valence 0.81 vs target 0.85 +0.14

#3  Gym Hero by Max Pulse
    Score: 0.72 / 1.00
    Reasons:
      - genre matches (pop) +0.10
      - energy 0.93 vs target 0.90 +0.29
      - acousticness 0.05 vs target 0.10 +0.19
      - valence 0.77 vs target 0.85 +0.14

#4  Laser Garden by Pixel Tide
    Score: 0.62 / 1.00
    Reasons:
      - energy 0.95 vs target 0.90 +0.29
      - acousticness 0.03 vs target 0.10 +0.19
      - valence 0.88 vs target 0.85 +0.15

#5  Storm Runner by Voltline
    Score: 0.59 / 1.00
    Reasons:
      - energy 0.91 vs target 0.90 +0.30
      - acousticness 0.10 vs target 0.10 +0.20
      - valence 0.48 vs target 0.85 +0.09
```

### Chill Lofi

```text
================================================================
CHILL LOFI - TOP 5
Profile: lofi / chill
================================================================

#1  Library Rain by Paper Lanterns
    Score: 0.98 / 1.00
    Reasons:
      - mood matches (chill) +0.25
      - genre matches (lofi) +0.10
      - energy 0.35 vs target 0.35 +0.30
      - acousticness 0.86 vs target 0.80 +0.19
      - valence 0.60 vs target 0.58 +0.15

#2  Midnight Coding by LoRoom
    Score: 0.96 / 1.00
    Reasons:
      - mood matches (chill) +0.25
      - genre matches (lofi) +0.10
      - energy 0.42 vs target 0.35 +0.28
      - acousticness 0.71 vs target 0.80 +0.18
      - valence 0.56 vs target 0.58 +0.15

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 0.84 / 1.00
    Reasons:
      - mood matches (chill) +0.25
      - energy 0.28 vs target 0.35 +0.28
      - acousticness 0.92 vs target 0.80 +0.18
      - valence 0.65 vs target 0.58 +0.14

#4  Focus Flow by LoRoom
    Score: 0.73 / 1.00
    Reasons:
      - genre matches (lofi) +0.10
      - energy 0.40 vs target 0.35 +0.28
      - acousticness 0.78 vs target 0.80 +0.20
      - valence 0.59 vs target 0.58 +0.15

#5  Dusty Porch Light by Willow Creek
    Score: 0.61 / 1.00
    Reasons:
      - energy 0.48 vs target 0.35 +0.26
      - acousticness 0.82 vs target 0.80 +0.20
      - valence 0.58 vs target 0.58 +0.15
```

### Deep Intense Rock

```text
================================================================
DEEP INTENSE ROCK - TOP 5
Profile: rock / intense
================================================================

#1  Storm Runner by Voltline
    Score: 0.98 / 1.00
    Reasons:
      - mood matches (intense) +0.25
      - genre matches (rock) +0.10
      - energy 0.91 vs target 0.92 +0.30
      - acousticness 0.10 vs target 0.08 +0.20
      - valence 0.48 vs target 0.40 +0.14

#2  Gym Hero by Max Pulse
    Score: 0.84 / 1.00
    Reasons:
      - mood matches (intense) +0.25
      - energy 0.93 vs target 0.92 +0.30
      - acousticness 0.05 vs target 0.08 +0.19
      - valence 0.77 vs target 0.40 +0.09

#3  Iron Cathedral by Black Harbor
    Score: 0.60 / 1.00
    Reasons:
      - energy 0.97 vs target 0.92 +0.29
      - acousticness 0.04 vs target 0.08 +0.19
      - valence 0.25 vs target 0.40 +0.13

#4  Concrete Crown by Kid Meridian
    Score: 0.57 / 1.00
    Reasons:
      - energy 0.78 vs target 0.92 +0.26
      - acousticness 0.12 vs target 0.08 +0.19
      - valence 0.62 vs target 0.40 +0.12

#5  Laser Garden by Pixel Tide
    Score: 0.56 / 1.00
    Reasons:
      - energy 0.95 vs target 0.92 +0.29
      - acousticness 0.03 vs target 0.08 +0.19
      - valence 0.88 vs target 0.40 +0.08
```

### Conflict: High Energy + Sad Mood

```text
================================================================
CONFLICT: HIGH ENERGY + SAD MOOD - TOP 5
Profile: pop / sad
================================================================

#1  Gym Hero by Max Pulse
    Score: 0.63 / 1.00
    Reasons:
      - genre matches (pop) +0.10
      - energy 0.93 vs target 0.90 +0.29
      - acousticness 0.05 vs target 0.10 +0.19
      - valence 0.77 vs target 0.10 +0.05

#2  Sunrise City by Neon Echo
    Score: 0.60 / 1.00
    Reasons:
      - genre matches (pop) +0.10
      - energy 0.82 vs target 0.90 +0.28
      - acousticness 0.18 vs target 0.10 +0.18
      - valence 0.84 vs target 0.10 +0.04

#3  Iron Cathedral by Black Harbor
    Score: 0.59 / 1.00
    Reasons:
      - energy 0.97 vs target 0.90 +0.28
      - acousticness 0.04 vs target 0.10 +0.19
      - valence 0.25 vs target 0.10 +0.13

#4  Storm Runner by Voltline
    Score: 0.59 / 1.00
    Reasons:
      - energy 0.91 vs target 0.90 +0.30
      - acousticness 0.10 vs target 0.10 +0.20
      - valence 0.48 vs target 0.10 +0.09

#5  Concrete Crown by Kid Meridian
    Score: 0.53 / 1.00
    Reasons:
      - energy 0.78 vs target 0.90 +0.26
      - acousticness 0.12 vs target 0.10 +0.20
      - valence 0.62 vs target 0.10 +0.07
```

### Conflict: Angry Mood + Acoustic + Calm

```text
================================================================
CONFLICT: ANGRY MOOD + ACOUSTIC + CALM - TOP 5
Profile: metal / angry
================================================================

#1  Pine Smoke Morning by Hollow Fern
    Score: 0.55 / 1.00
    Reasons:
      - energy 0.30 vs target 0.10 +0.24
      - acousticness 0.93 vs target 0.95 +0.20
      - valence 0.69 vs target 0.90 +0.12

#2  Spacewalk Thoughts by Orbit Bloom
    Score: 0.55 / 1.00
    Reasons:
      - energy 0.28 vs target 0.10 +0.25
      - acousticness 0.92 vs target 0.95 +0.19
      - valence 0.65 vs target 0.90 +0.11

#3  Coffee Shop Stories by Slow Stereo
    Score: 0.53 / 1.00
    Reasons:
      - energy 0.37 vs target 0.10 +0.22
      - acousticness 0.89 vs target 0.95 +0.19
      - valence 0.71 vs target 0.90 +0.12

#4  Moonlit Sonata Redux by Elena Voss
    Score: 0.53 / 1.00
    Reasons:
      - energy 0.22 vs target 0.10 +0.26
      - acousticness 0.95 vs target 0.95 +0.20
      - valence 0.31 vs target 0.90 +0.06

#5  Library Rain by Paper Lanterns
    Score: 0.51 / 1.00
    Reasons:
      - energy 0.35 vs target 0.10 +0.22
      - acousticness 0.86 vs target 0.95 +0.18
      - valence 0.60 vs target 0.90 +0.10
```

### Unknown Genre And Mood

```text
================================================================
UNKNOWN GENRE AND MOOD - TOP 5
Profile: k-pop / dreamy
================================================================

#1  Island Drift by Sunday Roots
    Score: 0.59 / 1.00
    Reasons:
      - energy 0.52 vs target 0.50 +0.29
      - acousticness 0.47 vs target 0.50 +0.19
      - valence 0.80 vs target 0.50 +0.10

#2  Velvet Hours by Sade Marlowe
    Score: 0.58 / 1.00
    Reasons:
      - energy 0.55 vs target 0.50 +0.28
      - acousticness 0.34 vs target 0.50 +0.17
      - valence 0.67 vs target 0.50 +0.12

#3  Midnight Coding by LoRoom
    Score: 0.57 / 1.00
    Reasons:
      - energy 0.42 vs target 0.50 +0.28
      - acousticness 0.71 vs target 0.50 +0.16
      - valence 0.56 vs target 0.50 +0.14

#4  Dusty Porch Light by Willow Creek
    Score: 0.57 / 1.00
    Reasons:
      - energy 0.48 vs target 0.50 +0.29
      - acousticness 0.82 vs target 0.50 +0.14
      - valence 0.58 vs target 0.50 +0.14

#5  Focus Flow by LoRoom
    Score: 0.55 / 1.00
    Reasons:
      - energy 0.40 vs target 0.50 +0.27
      - acousticness 0.78 vs target 0.50 +0.14
      - valence 0.59 vs target 0.50 +0.14
```

### Case/Whitespace Mismatch

```text
================================================================
CASE/WHITESPACE MISMATCH - TOP 5
Profile: Pop  / Happy
================================================================

#1  Sunrise City by Neon Echo
    Score: 0.63 / 1.00
    Reasons:
      - energy 0.82 vs target 0.80 +0.29
      - acousticness 0.18 vs target 0.20 +0.20
      - valence 0.84 vs target 0.80 +0.14

#2  Rooftop Lights by Indigo Parade
    Score: 0.61 / 1.00
    Reasons:
      - energy 0.76 vs target 0.80 +0.29
      - acousticness 0.35 vs target 0.20 +0.17
      - valence 0.81 vs target 0.80 +0.15

#3  Concrete Crown by Kid Meridian
    Score: 0.60 / 1.00
    Reasons:
      - energy 0.78 vs target 0.80 +0.29
      - acousticness 0.12 vs target 0.20 +0.18
      - valence 0.62 vs target 0.80 +0.12

#4  Night Drive Loop by Neon Echo
    Score: 0.58 / 1.00
    Reasons:
      - energy 0.75 vs target 0.80 +0.28
      - acousticness 0.22 vs target 0.20 +0.20
      - valence 0.49 vs target 0.80 +0.10

#5  Gym Hero by Max Pulse
    Score: 0.58 / 1.00
    Reasons:
      - energy 0.93 vs target 0.80 +0.26
      - acousticness 0.05 vs target 0.20 +0.17
      - valence 0.77 vs target 0.80 +0.15
```

### Out-Of-Range Targets

```text
================================================================
OUT-OF-RANGE TARGETS - TOP 5
Profile: edm / euphoric
================================================================

#1  Laser Garden by Pixel Tide
    Score: 0.55 / 1.00
    Reasons:
      - mood matches (euphoric) +0.25
      - genre matches (edm) +0.10
      - energy 0.95 vs target 1.80 +0.04
      - acousticness 0.03 vs target -0.50 +0.09
      - valence 0.88 vs target 1.50 +0.06

#2  Gym Hero by Max Pulse
    Score: 0.17 / 1.00
    Reasons:
      - energy 0.93 vs target 1.80 +0.04
      - acousticness 0.05 vs target -0.50 +0.09
      - valence 0.77 vs target 1.50 +0.04

#3  Sunrise City by Neon Echo
    Score: 0.12 / 1.00
    Reasons:
      - energy 0.82 vs target 1.80 +0.01
      - acousticness 0.18 vs target -0.50 +0.06
      - valence 0.84 vs target 1.50 +0.05

#4  Storm Runner by Voltline
    Score: 0.11 / 1.00
    Reasons:
      - energy 0.91 vs target 1.80 +0.03
      - acousticness 0.10 vs target -0.50 +0.08
      - valence 0.48 vs target 1.50 +-0.00

#5  Iron Cathedral by Black Harbor
    Score: 0.11 / 1.00
    Reasons:
      - energy 0.97 vs target 1.80 +0.05
      - acousticness 0.04 vs target -0.50 +0.09
      - valence 0.25 vs target 1.50 +-0.04

================================================================
```

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



