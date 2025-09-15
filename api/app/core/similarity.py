from typing import List, Optional
import os
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        name = os.getenv('MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
        _model = SentenceTransformer(name, device='cpu')
    return _model

def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_model()
    vecs = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, batch_size=32)
    # Ensure L2-normalized
    vecs = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)
    return vecs

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a)+1e-12) / (np.linalg.norm(b)+1e-12))
