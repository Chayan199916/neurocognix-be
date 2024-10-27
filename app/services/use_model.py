import tensorflow_hub as hub
from typing import Optional
import numpy as np


class USEModel:
    _instance: Optional['USEModel'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(USEModel, cls).__new__(cls)
            cls._instance.model = None
        return cls._instance

    def load_model(self, module_url: str) -> None:
        """Load the Universal Sentence Encoder model"""
        if self.model is None:
            print(f"Loading Universal Sentence Encoder from {module_url}")
            self.model = hub.load(module_url)
            print("Model loaded successfully")

    def get_embeddings(self, texts: list) -> np.ndarray:
        """Get embeddings for a list of texts"""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model first.")
        return self.model(texts).numpy()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        embeddings = self.get_embeddings([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)
