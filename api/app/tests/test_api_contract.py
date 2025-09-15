import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope='session', autouse=True)
def set_env():
    os.environ.setdefault('MONGO_URL', 'mongodb://localhost:27017/word-detective-lite')
    os.environ.setdefault('DAILY_SEED_SALT', 'test-salt')
    os.environ.setdefault('CORS_ORIGINS', 'http://localhost:5173')
    os.environ.setdefault('MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')

def test_api_contract_happy_path():
    client = TestClient(app)
    # health
    r = client.get('/api/health')
    assert r.status_code == 200 and r.json()['ok'] is True

    # create daily game
    r = client.post('/api/game', json={'mode': 'daily'})
    assert r.status_code == 200
    game = r.json()
    gid = game['gameId']

    # invalid guess (OOV - use word unlikely to exist)
    r = client.post('/api/guess', json={'gameId': gid, 'word': 'zzzzzzzzzz'})
    assert r.status_code == 400
    assert r.json()['error']['code'] in ('OOV','INVALID_WORD')

    # valid in-vocab guess: pick first word
    from pathlib import Path
    words = Path(__file__).resolve().parents[2] / 'data' / 'words.txt'
    first = words.read_text(encoding='utf-8').splitlines()[0]
    r = client.post('/api/guess', json={'gameId': gid, 'word': first})
    assert r.status_code == 200
    body = r.json()
    assert 'similarity' in body and 'band' in body and 'attempts' in body

    # fetch game
    r = client.get(f'/api/game/{gid}')
    assert r.status_code == 200
    g = r.json()
    assert 'lastGuesses' in g
    assert len(g['lastGuesses']) >= 1
