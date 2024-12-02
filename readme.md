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

## Core Components

### 1. Config Classes

#### `Config`

Purpose: Stores global configuration constants

- `MODULE_URL`: URL for Universal Sentence Encoder model
- `STS_DATASET_URL`: URL for semantic textual similarity dataset

#### `GameConfig`

Purpose: Manages game-specific configuration parameters

```python
Constants:
- `MIN_DIFFICULTY`: Minimum difficulty level (3)
- `MAX_DIFFICULTY`: Maximum difficulty level (10)
- `BASE_TIME_PER_WORD`: Base time allowed per word (1.0 seconds)
- `TRANSITION_TIME`: Time between sequences (0.5 seconds)
- `SEMANTIC_THRESHOLD`: Threshold for semantic similarity (0.7)
- `EMA_ALPHA`: Exponential Moving Average smoothing factor (0.2)
- `DIFFICULTY_INCREASE_THRESHOLD`: Performance threshold for increasing difficulty (1.2)
- `DIFFICULTY_DECREASE_THRESHOLD`: Performance threshold for decreasing difficulty (0.8)
- `COGNITIVE_LOAD_INCREMENT`: Rate of cognitive load increase (0.05)
- `FATIGUE_INCREMENT`: Rate of fatigue increase (0.025)
- `MAX_CONSECUTIVE_FAILURES`: Maximum allowed consecutive failures (3)
```

### 2. Core Classes

#### `WordAnalyzer`

Purpose: Analyzes word complexity and characteristics

Methods:

- `count_syllables(word: str) -> int`

  - Uses CMU pronunciation dictionary to count syllables
  - Fallback to vowel counting if word not found

- `calculate_complexity(word: str) -> float`
  - Formula: `0.4 * (syllables/4) + 0.3 * (length/10) + 0.3 * (unique_letters/10)`
  - Weights: Syllables (40%), Length (30%), Unique letters (30%)
  - Returns normalized complexity score between 0.2 and 1.0

#### `AdaptiveTimeManager`

Purpose: Manages response time expectations and adaptations.

Methods:

- `update_ema(new_time: float) -> None`

  - Updates exponential moving average of response times
  - Formula: `EMA = α * new_value + (1-α) * EMA_previous`

- `calculate_expected_time(sequence: List[str], cognitive_load: float, fatigue: float) -> float`
  - Calculates expected completion time based on:
    - Base time per word
    - Cognitive load factor (20% impact)
    - Fatigue factor (15% impact)
    - Historical performance (±20% adjustment)
  - Formula: `base_time * cognitive_factor * fatigue_factor * performance_factor`
  - Where:
    - `base_time = sequence_length * BASE_TIME_PER_WORD`
    - `cognitive_factor = 1 + (cognitive_load * 0.2)`
    - `fatigue_factor = 1 + (fatigue * 0.15)`
    - `performance_factor = min(1.5, max(0.8, ema_response_time/base_time))`

#### `DifficultyManager`

Purpose: Manages dynamic difficulty adjustment.

Methods:

- `adjust_difficulty(recent_score: int, target_score: int) -> str`
  - Uses rolling average of last 3 scores
  - Increases difficulty if avg_score > target_score \* 1.2
  - Decreases difficulty after 3 consecutive poor performances
  - Maintains bounds between MIN_DIFFICULTY and MAX_DIFFICULTY

#### `ProfileManager`

Purpose: Manages user profiles and difficulty adjustments.

Constants:

```python
AGE_FACTORS = {'child': -1, 'teen': 0, 'adult': 1, 'senior': 0}
EDUCATION_FACTORS = {'elementary': -1, 'high_school': 0, 'college': 1, 'graduate': 2}
LANGUAGE_FACTORS = {'beginner': -1, 'intermediate': 0, 'advanced': 1, 'native': 2}
```

Methods:

- `select_categories() -> List[str]`
  - Returns age-appropriate word categories
- `calculate_difficulty_adjustment() -> int`
  - Combines age, education, and language factors for initial difficulty

### 3. Main Game Class

#### `NeuroCognixGame`

Purpose: Core game logic and state management

Key Components:

1. Score Calculation

   ```python
   final_score = base_score + time_bonus - cognitive_penalty - fatigue_penalty
   Where:
   ```

- base_score = difficulty_level \* 10
- time_bonus = base_score \* 0.5 \_ (expected_time - response_time)/expected_time
- cognitive*penalty = base_score * (cognitive*load * 0.3)
- fatigue*penalty = base_score * (fatigue*factor * 0.2)

Bounds:

- Minimum score: 20% of base_score
- Maximum score: 200% of base_score

2. Word Similarity Checking

Methods: 1. Exact match 2. Levenshtein distance (≤ 1 for typos) 3. Semantic similarity using Universal Sentence Encoder

- Cosine similarity formula: `cos(θ) = (A·B)/(||A||·||B||)`
- Threshold: 0.7 (configurable)

3. Cognitive State Management
   - Incremental increase in cognitive load
   - Fatigue accumulation over time
   - Dynamic difficulty adjustment

Updated after each sequence:

```python
cognitive_load = min(1.0, cognitive_load + COGNITIVE_LOAD_INCREMENT)
fatigue_factor = min(1.0, fatigue_factor + FATIGUE_INCREMENT)
```

### 4. Data Structures

#### Word Categories

Organized by themes:

- fruits
- colors
- animals
- professions
- countries
- household_items
- body_parts
- vehicles
- emotions

Each category contains 18 carefully selected words with varying complexity levels.

### 5. Machine Learning Components

#### Universal Sentence Encoder

- Purpose: Semantic similarity analysis
- Model URL: "https://tfhub.dev/google/universal-sentence-encoder/4"
- Output: 512-dimensional embeddings
- Used for: Advanced word similarity checking

## Performance Optimization

### Time Complexity

- Word similarity checking: O(1) for exact match, O(n) for Levenshtein
- Sequence generation: O(n log n) due to sorting by complexity
- Score calculation: O(1)

### Space Complexity

- Word categories: O(n) where n is total number of words
- Player history: O(m) where m is number of played rounds
- Embeddings cache: O(k) where k is number of unique words used

## Error Handling

- Graceful fallback for pronunciation dictionary
- Bounded score calculations
- Protected against division by zero in time calculations
- Input validation for all user inputs

Methods:

- `generate_sequence() -> str`
- `calculate_score(is_correct: bool, response_time: float) -> int`
- `check_answer(player_input: str, start_time: float, end_time: float) -> Tuple[bool, int, List[str]]`
- `verify_sequence(player_input: str) -> bool`
- `generate_feedback(player_input: str) -> List[str]`
- `update_cognitive_state() -> None`

## Key Algorithms and Logic

### 1. Difficulty Adaptation

- Uses moving average of last 3 scores
- Adjusts based on performance thresholds
- Considers consecutive failures
- Incorporates player profile factors

### 2. Score Calculation

- Base score from difficulty
- Time bonus for quick responses
- Penalties for cognitive load and fatigue
- Bonus points for sequence length
- Modifiers based on player state

### 3. Word Complexity

- Syllable count
- Word length
- Unique letters
- Weighted combination for final complexity

### 4. Response Evaluation

- Multiple similarity checks
- Semantic analysis using USE
- Typo tolerance
- Detailed feedback generation

### 5. Cognitive Load Management

- Incremental increase during gameplay
- Impact on timing expectations
- Influence on scoring
- Recovery mechanisms

## Implementation Notes

1. Error Handling

   - Global error handler
   - Input validation
   - Type checking
   - Exception management

2. Performance Optimization

   - Caching of word complexities
   - Efficient similarity checking
   - Optimized score calculations

3. Extensibility

   - Modular design
   - Configurable parameters
   - Flexible category system
   - Adaptable difficulty mechanics

4. Security Considerations
   - Input sanitization
   - CORS configuration
   - Error message safety
   - Rate limiting considerations

## Future Enhancements

1. Additional word categories
2. Multi-language support
3. Persistent user profiles
4. Advanced analytics dashboard
5. Multiplayer mode

```

```
