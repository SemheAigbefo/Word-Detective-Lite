import os
import asyncio
from datetime import datetime, timezone, date
from typing import List

import numpy as np
from fastapi import FastAPI, Response, Depends, Cookie, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from bson import ObjectId

from .models import *
from .db import init_db, games, guesses
from .deps import ensure_session, COOKIE_NAME
from .core.normalize import normalize_word
from .core.bands import band_for
from .core.daily_seed import target_index_for
from .core.similarity import embed_texts

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/word-detective-lite')
DAILY_SEED_SALT = os.getenv('DAILY_SEED_SALT', 'change-me')
CORS_ORIGINS = [o.strip() for o in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',') if o.strip()]

WORDS: List[str] = []
VECTORS: np.ndarray | None = None

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.on_event('startup')
async def startup():
    global WORDS, VECTORS
    # DB
    await init_db()
    # Data
    from pathlib import Path
    data_dir = Path(__file__).resolve().parents[1] / 'data'
    words_path = data_dir / 'words.txt'
    emb_path = data_dir / 'embeddings.npz'
    WORDS = [w.strip() for w in words_path.read_text(encoding='utf-8').splitlines() if w.strip()]
    VECTORS = np.load(emb_path)['vectors']
    if len(WORDS) != VECTORS.shape[0]:
        raise RuntimeError('words.txt and embeddings length mismatch')
    # Ensure normalized
    norms = np.linalg.norm(VECTORS, axis=1, keepdims=True) + 1e-12
    VECTORS = VECTORS / norms

def error(code: str, message: str, status: int = 400):
    return JSONResponse(status_code=status, content={'error': {'code': code, 'message': message}})

@app.get('/api/health')
async def health():
    return {'ok': True}

@app.post('/api/game')
async def create_game(payload: CreateGameRequest, response: Response, session_id: str | None = Cookie(default=None, alias=COOKIE_NAME)):
    sid = ensure_session(response, session_id)
    mode = payload.mode
    # choose target index
    if mode == 'daily':
        today = date.today().isoformat()
        idx = target_index_for(today, DAILY_SEED_SALT, len(WORDS))
        daily_date = today
    else:
        import random
        idx = random.randrange(len(WORDS))
        daily_date = None
    doc = {
        'sessionId': sid,
        'mode': mode,
        'targetIndex': idx,
        'startedAt': datetime.now(timezone.utc),
        'completedAt': None,
        'attempts': 0,
        'dailyDate': daily_date
    }
    res = await games.insert_one(doc)
    return {
        'gameId': str(res.inserted_id),
        'mode': mode,
        'startedAt': doc['startedAt'].isoformat()
    }

@app.get('/api/game/{id}')
async def get_game(id: str, response: Response, session_id: str | None = Cookie(default=None, alias=COOKIE_NAME)):
    sid = ensure_session(response, session_id)
    try:
        oid = ObjectId(id)
    except Exception:
        return error('BAD_ID', 'invalid game id', 400)
    game = await games.find_one({'_id': oid, 'sessionId': sid})
    if not game:
        return error('NOT_FOUND', 'game not found', 404)
    cur = guesses.find({'gameId': str(oid)}, sort=[('createdAt', -1)], limit=10)
    last = []
    async for g in cur:
        last.append({
            'normalizedWord': g['normalizedWord'],
            'similarity': g['similarity'],
            'band': g['band'],
            'isCorrect': g['isCorrect'],
            'at': g['createdAt'].isoformat()
        })
    return {
        'gameId': str(game['_id']),
        'mode': game['mode'],
        'startedAt': game['startedAt'].isoformat(),
        'attempts': game['attempts'],
        'lastGuesses': last
    }

@app.post('/api/guess')
async def post_guess(payload: GuessRequest, response: Response, session_id: str | None = Cookie(default=None, alias=COOKIE_NAME)):
    sid = ensure_session(response, session_id)
    # validate game
    try:
        oid = ObjectId(payload.gameId)
    except Exception:
        return error('BAD_ID', 'invalid game id', 400)
    game = await games.find_one({'_id': oid, 'sessionId': sid})
    if not game:
        return error('NOT_FOUND', 'game not found', 404)

    word_norm = normalize_word(payload.word)
    if not word_norm:
        return error('INVALID_WORD', 'word must contain only letters', 400)
    try:
        idx = WORDS.index(word_norm)
    except ValueError:
        return error('OOV', 'word not in vocabulary', 400)

    # compute similarity to target vector only
    target_vec = VECTORS[game['targetIndex']]
    guess_vec = (await asyncio.get_event_loop().run_in_executor(None, lambda: None)) or None
    # embed guess
    from .core.similarity import embed_texts
    guess_vec = embed_texts([word_norm])[0]
    sim = float(np.dot(guess_vec, target_vec))  # both normalized

    band = band_for(sim)
    is_correct = (word_norm == WORDS[game['targetIndex']])
    attempts = int(game.get('attempts', 0)) + 1
    await games.update_one({'_id': oid}, {'$set': {'attempts': attempts}})

    doc = {
        'gameId': str(oid),
        'sessionId': sid,
        'word': payload.word,
        'normalizedWord': word_norm,
        'similarity': sim,
        'band': band,
        'isCorrect': is_correct,
        'createdAt': datetime.now(timezone.utc)
    }
    await guesses.insert_one(doc)

    return {
        'normalizedWord': word_norm,
        'similarity': sim,
        'band': band,
        'attempts': attempts,
        'isCorrect': is_correct
    }
