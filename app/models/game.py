import random
import math
import numpy as np
from Levenshtein import distance as levenshtein_distance
from typing import Dict, List, Tuple, Optional
from ..services.use_model import USEModel


class GameState:
    def __init__(self):
        self.cognitive_load = 0.0
        self.fatigue_factor = 0.0
        self.score = 0
        self.score_history: List[int] = []
        self.response_time_history: List[float] = []
        self.ema_response_time: Optional[float] = None
        self.difficulty_adjusted = False
        self.profile_difficulty_set = False


class NeuroCognixGame:
    def __init__(self):
        self.use_model = USEModel()
        self.state = GameState()
        self.difficulty = 5
        self.min_difficulty = 3
        self.max_difficulty = 10
        self.sequence: List[str] = []
        self.current_category = ''
        self.semantic_similarity_threshold = 0.7
        self.alpha = 0.2  # EMA smoothing factor
        self.categories = self._initialize_categories()
        self.word_frequency_data = self._initialize_word_frequency()

        # Player profile
        self.age_group: Optional[str] = None
        self.education_level: Optional[str] = None
        self.language_proficiency: Optional[str] = None

    def _initialize_categories(self) -> Dict[str, List[str]]:
        return {
            'fruits': ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape'],
            'colors': ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black'],
            'animals': ['cat', 'dog', 'elephant', 'giraffe', 'lion', 'tiger', 'bear'],
            # ... [rest of categories] ...
        }

    def _initialize_word_frequency(self) -> Dict[str, int]:
        return {word: random.randint(1, 1000)
                for category in self.categories.values()
                for word in category}

    def set_player_profile(self, age_group: str, education_level: str,
                           language_proficiency: str) -> None:
        self.age_group = age_group
        self.education_level = education_level
        self.language_proficiency = language_proficiency
        self.state.profile_difficulty_set = False

    def check_sequence(self, player_input: str) -> bool:
        player_words = player_input.lower().split()
        if len(player_words) != len(self.sequence):
            return False

        return all(self._is_word_similar(orig.lower(), player)
                   for orig, player in zip(self.sequence, player_words))

    def _is_word_similar(self, original: str, player_word: str) -> bool:
        if original == player_word:
            return True
        if levenshtein_distance(original, player_word) <= 1:
            return True
        return self.use_model.calculate_similarity(original, player_word) > self.semantic_similarity_threshold

    def calculate_score(self, start_time: float, end_time: float) -> int:
        response_time = max(0.1, end_time - start_time)
        self.state.response_time_history.append(response_time)

        # Update EMA
        if self.state.ema_response_time is None:
            self.state.ema_response_time = response_time
        else:
            self.state.ema_response_time = (self.alpha * response_time +
                                            (1 - self.alpha) * self.state.ema_response_time)

        expected_time = self.calculate_expected_time()
        time_factor = max(
            0, min(2, 2 - (self.state.ema_response_time / expected_time)))
        difficulty_factor = self.difficulty / self.max_difficulty

        base_score = 100 * len(self.sequence)
        score = int(base_score * time_factor * difficulty_factor)

        self.state.score += score
        self.state.score_history.append(score)

        return score

    def calculate_expected_time(self) -> float:
        BASE_TIME = 1.0
        TRANSITION_TIME = 0.5

        def word_complexity(word: str) -> float:
            return max(0.8, min(1.5, math.log(len(word)) / 2))

        total_time = sum(
            BASE_TIME * word_complexity(word) *
            (1 + (i / len(self.sequence)) * 0.2)
            + TRANSITION_TIME
            for i, word in enumerate(self.sequence)
        )

        fatigue_factor = 1 + (self.state.fatigue_factor * 0.05)
        cognitive_load_factor = 1 + (self.state.cognitive_load * 0.1)

        return total_time * fatigue_factor * cognitive_load_factor

    # ... [Additional methods would continue here] ...
