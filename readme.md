# NeuroCognix Game Backend

**NeuroCognix** is an adaptive cognitive training game designed to enhance memory, language processing, and pattern recognition. It dynamically adjusts difficulty based on player performance, accounting for cognitive load and fatigue, to create a personalized training experience.

---

## 🧠 Core Algorithm Design

### 1. Adaptive Difficulty System

The game uses a multi-factor adaptive difficulty system based on:

- **Player Performance**: Score history
- **Response Times**: Smoothed with Exponential Moving Average (EMA)
- **Player Profile**: Age, education, and language proficiency
- **Cognitive Load Accumulation**
- **Fatigue Factor**

**Difficulty Adjustment Formula:**

```python
adjusted_difficulty = base_difficulty + performance_factor + (cognitive_load * 0.1) - (fatigue_factor * 0.05)
```

### 2. Word Selection Algorithm

**Words are chosen according to:**

- Word Frequency: Common vs. rare words
- Word Length and Complexity
- Category Appropriateness: Tailored to player profile
- Current Cognitive Load
- Fatigue Level

### 3. Scoring System

**The scoring mechanism considers:**

- Sequence Length
- Response Time: Compared to expected time
- Current Difficulty Level
- Word Complexity

**Score Formula:**

```python
score = base_score * time_factor * difficulty_factor
```

where:

```python
base_score = 100 * sequence_length
time_factor = max(0, min(2, 2 - (actual_time / expected_time)))
difficulty_factor = current_difficulty / max_difficulty
```

### 4. Response Time Analysis

Response time analysis uses Exponential Moving Average (EMA) for smoothing and adaptive expected time calculations, factoring in:

- Word Length
- Word Complexity
- Sequence Position
- Current Cognitive Load
- Fatigue Factor

### 5. Answer Validation

**Three-layer validation to ensure accurate assessment:**

- Exact Match
- Levenshtein Distance: Accounts for minor typos
- Semantic Similarity: Using Universal Sentence Encoder

### 🎮 API Endpoints

This table describes the available API endpoints for this project.

| Endpoint           | Method | Description                                                |
| ------------------ | ------ | ---------------------------------------------------------- |
| /start-game        | POST   | Initializes a new game session with player profile.        |
| /submit-answer     | POST   | Processes player answers and returns performance metrics.  |
| /generate-sequence | GET    | Generates a new word sequence based on current game state. |
| /player-stats      | GET    | Returns player performance statistics.                     |
| /leaderboard       | GET    | Retrieves global leaderboard data.                         |
