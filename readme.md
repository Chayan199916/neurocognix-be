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
- MIN_DIFFICULTY = 3
- MAX_DIFFICULTY = 10
- BASE_TIME_PER_WORD = 1.0
- TRANSITION_TIME = 0.5
- SEMANTIC_THRESHOLD = 0.7
- EMA_ALPHA = 0.2
- DIFFICULTY_INCREASE_THRESHOLD = 1.2
- DIFFICULTY_DECREASE_THRESHOLD = 0.8
- COGNITIVE_LOAD_INCREMENT = 0.05
- FATIGUE_INCREMENT = 0.025
- MAX_CONSECUTIVE_FAILURES = 3
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
  - Returns normalized complexity score between 0.2 and 1.0

#### `AdaptiveTimeManager`

Purpose: Manages response time expectations and tracking

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

#### `DifficultyManager`

Purpose: Manages game difficulty adaptation

Methods:

- `adjust_difficulty(recent_score: int, target_score: int) -> str`
  - Uses 3-round moving average for stability
  - Increases difficulty if performance > 120% of target
  - Decreases difficulty after 3 consecutive poor performances
  - Maintains bounds between MIN_DIFFICULTY and MAX_DIFFICULTY

#### `ProfileManager`

Purpose: Manages player profiles and customization

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
   where:
   - base_score = difficulty * 10
   - time_bonus = up to 50% of base_score
   - cognitive_penalty = up to 30% reduction
   - fatigue_penalty = up to 20% reduction
   ```

2. Word Similarity Checking

   - Exact match
   - Levenshtein distance for typos (≤1)
   - Semantic similarity using Universal Sentence Encoder

3. Cognitive State Management
   - Incremental increase in cognitive load
   - Fatigue accumulation over time
   - Dynamic difficulty adjustment

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
