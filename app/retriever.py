import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple

class InMemoryRetriever:
    def __init__(self, embeddings: np.ndarray, metadata: List[Dict[str,Any]]):
        # embeddings: N x D, metadata: list of dicts (text, page, ...)
        self.embeddings = embeddings
        self.metadata = metadata

    def query(self, q_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict,str,float]]:
        # q_embedding: (1,D)
        sims = cosine_similarity(self.embeddings, q_embedding.reshape(1, -1)).reshape(-1)
        idx = np.argsort(-sims)[:top_k]
        results = []
        for i in idx:
            meta = self.metadata[i].copy()
            meta['score'] = float(sims[i])
            results.append((meta, meta.get('text',''), float(sims[i])))
        return results
