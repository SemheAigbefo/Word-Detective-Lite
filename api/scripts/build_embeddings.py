import os
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.getenv('MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / 'data' / 'words.txt'
EMB = ROOT / 'data' / 'embeddings.npz'

def normalize_word(s: str) -> str:
    s = s.strip().lower()
    if not re.fullmatch(r'[a-z]+', s):
        return ''
    return s

def main():
    words = []
    seen = set()
    for line in WORDS.read_text(encoding='utf-8').splitlines():
        w = normalize_word(line)
        if not w or w in seen:
            continue
        seen.add(w)
        words.append(w)
    # rewrite words in canonical order
    WORDS.write_text('\n'.join(words), encoding='utf-8')

    model = SentenceTransformer(MODEL_NAME, device='cpu')
    vecs = model.encode(words, convert_to_numpy=True, normalize_embeddings=True, batch_size=256)
    # Ensure L2-normalized
    vecs = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)
    np.savez_compressed(EMB, vectors=vecs)
    print(f'Wrote {EMB} for {len(words)} words, dim={vecs.shape[1]}')

if __name__ == '__main__':
    main()
