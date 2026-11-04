# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

A small, simple music recommender. It matches songs to a taste profile.

---

## 2. Intended Use  

**Goal:** guess which songs from a small list a person would like, based on their favorite mood, genre, and how loud, acoustic, and happy they want the music.

**Designed for:**

- Classroom practice and learning how recommenders work.
- Showing the score for each song so people can see why it was picked.

**Assumes:** the user can describe their taste with five settings. It does not learn from listening history.

**Not for:**

- Real music apps or real users. The song list is far too small.
- Judging anyone's taste or mood. It only matches numbers and labels.
- Songs outside the 18 in the list.

---

## 3. How the Model Works  

It scores every song against a taste profile and returns the top five. Each song gets up to 1.0 points.

- Mood match: 0.25. Genre match: 0.10. All or nothing.
- Energy (0.30), acousticness (0.20), valence (0.15): the closer to the user's target, the more points.
- Each pick shows its reasons, like "mood matches (happy) +0.25".

I also tried energy x2 and genre x0.5, scaled to still add up to 1.0. That version is in the code now. Undo it with `git checkout src/recommender.py`.

---

## 4. Data  

- 18 made-up songs in `data/songs.csv`.
- 15 genres and 13 moods. Most have just 1 song. There is no "sad" mood.
- Tempo and danceability are in the file but not used.
- No lyrics, language, or listening history.

---

## 5. Strengths  

- Works well when mood, genre, and energy agree. Pop, Lofi, and Rock all got the #1 I expected.
- Loud and quiet users get very different lists.
- The reasons make it easy to spot mistakes.

---

## 6. Limitations and Bias 

**Weakness:** energy counts too much and mood of the song counts too little. Energy and acousticness move together in this data, so they act like one "loud vs. quiet" setting worth 0.50. Valence is only 0.15. A user who wanted high energy and a sad mood got Gym Hero first. No song is "sad", and the happiness gap cost Gym Hero only about 0.10. Gym Hero made the top 5 for five of the eight profiles.

---

## 7. Evaluation  

**Profiles I tested**

- Normal: High-Energy Pop, Chill Lofi, Deep Intense Rock.
- Tricky: high energy + "sad", angry + calm acoustic, k-pop/dreamy (not in the data), "Pop " with a typo, and targets outside 0 to 1.
- Results below use the original weights.

**What surprised me**

- Gym Hero kept showing up, even for people who never asked for it.
- The "sad" profile got a workout song as #1.
- "Pop " instead of "pop" dropped the top score from 0.96 to 0.63.
- Doubling energy barely changed the normal profiles but scrambled the tricky ones.

**Why Gym Hero keeps showing up**

The system is a checklist: mood, genre, energy, acoustic, happy. Gym Hero is pop, loud, and not acoustic. A Happy Pop fan gets a check on genre and energy. It only misses on mood. With just 18 songs, there are few other loud songs to beat it.

**Profile vs. profile**

- **Pop vs. Lofi:** Pop gets loud, bright songs. Lofi gets quiet, acoustic ones. Totally different, as it should be.
- **Pop vs. Rock:** Both want loud, so Gym Hero is in both. Mood splits them: Sunrise City (happy) for Pop, Storm Runner (intense) for Rock.
- **Lofi vs. Rock:** Opposites. No songs in common.
- **Pop vs. "sad":** Same energy target, but "sad" has no matching songs. It just gets the loudest ones, so Gym Hero wins.
- **Rock vs. angry + calm:** It picks quiet acoustic songs. The numbers beat the mood label, and Iron Cathedral (the angry one) never shows up.
- **Lofi vs. k-pop/dreamy:** Lofi's best is 0.98. k-pop/dreamy tops out at 0.59 and everything is close. Almost a coin flip.
- **Pop vs. "Pop " typo:** Same person, but the score drops. A real happy song ends up tied with songs that aren't happy.
- **Pop vs. out-of-range:** Scores crash from 0.96 to 0.55 at best. Energy 1.8 can't be matched.

---

## 8. Future Work  

- **Fix typos:** ignore capitals and extra spaces, so "Pop " counts as "pop".
- **Add more songs:** include sad and dark ones, and more than one per genre.
- **Give valence more weight:** so a sad user stops getting workout songs.

---

## 9. Personal Reflection  

**Biggest learning moment:** Gym Hero showing up everywhere. I thought genre was the problem. It wasn't. Energy was, and the data was too small to give other options.

**How AI helped:** It wrote code fast and helped me find tricky test profiles. It also caught that doubling energy made my weights add up to 1.25, not 1.0.

**When I double-checked it:** I ran the code and read the real output. One edit broke the file because of a formatting bug, and running it showed that right away. I also compared the rankings to my own ear.

**What surprised me:** Just five numbers and a sort feel like a real recommender. The "reasons" list helps a lot, because it makes the picks feel explained.

**What I'd try next:** more songs (especially sad ones), more weight on valence, fixing capital-letter typos, and a rule so one song can't fill so many lists.
