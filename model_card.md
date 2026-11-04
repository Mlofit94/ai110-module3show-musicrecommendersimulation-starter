# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender compares every song in the catalog to a simple taste profile and picks the closest matches. It does not use listening history, only what a song sounds like.

**What it looks at:** each song's mood, genre, energy, acousticness (how acoustic versus electronic it sounds), and valence (how positive it feels). The user's profile holds a favorite mood, a favorite genre, and a target level for energy, acousticness, and valence.

**How it scores:** every song earns points out of 1.0.

- A matching mood is worth 0.25 and a matching genre is worth 0.10, all or nothing.
- For energy (0.30), acousticness (0.20), and valence (0.15), the closer a song is to the user's target, the more points it gets. A song that is too high or too low loses points equally, so closer is better, not higher.

**How it picks:** it scores every song, sorts from highest to lowest, and returns the top five. Each pick comes with a plain-language list of reasons, such as "mood matches (happy) +0.25".

**Changes from the starter:** the starter returned empty results. I implemented CSV loading, the scoring rule, and the ranking, and I replaced the single "likes acoustic" setting with acousticness and valence targets.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
