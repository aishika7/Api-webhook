# Lightweight, dependency-light "embedding" for mock/testing using TF-IDF vectors.
# The module exposes a simple EmbeddingModel with fit_transform and transform methods.
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Optional

class EmbeddingModel:
    def __init__(self):
        self.vec = TfidfVectorizer(ngram_range=(1,2), max_features=512)
        self.fitted = False

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        X = self.vec.fit_transform(texts).toarray()
        self.fitted = True
        return X.astype('float32')

    def transform(self, texts: List[str]) -> np.ndarray:
        if not self.fitted:
            # fallback: fit on texts (safe for mock)
            return self.fit_transform(texts)
        X = self.vec.transform(texts).toarray()
        return X.astype('float32')
