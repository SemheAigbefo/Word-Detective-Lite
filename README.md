# Word Detective Lite
A tiny word-similarity guessing game. React client → FastAPI → MongoDB. Embeddings are loaded into memory at API startup.

```mermaid
flowchart LR
  A[React (Vite)] -- fetch (credentials: include) --> B[FastAPI]
  B -- Motor --> C[(MongoDB)]
  B -.-> D[Embeddings loaded at startup]
```
## Features
- Daily or Free Play modes
- Sentence-transformers (`all-MiniLM-L6-v2`) embeddings
- Cosine similarity banded into Cold/Cool/Warm/Hot/Very Hot
- Anonymous sessions via HttpOnly cookies
- MongoDB persistence for games and guesses
- Optional similarity sparkline

## Tech Stack
| Layer | Tech |
|---|---|
| Frontend | React + TypeScript (Vite), TanStack Query |
| Backend | FastAPI, Uvicorn |
| DB | MongoDB 7 (Motor async driver) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Container | Docker Compose |

## Quickstart

### Option A: Docker Compose
```bash
docker compose up --build
```
- Web: http://localhost:5173
- API: http://localhost:8000
- Mongo: mongodb://mongo:27017

### Option B: Local Dev
**API**
```bash
cd api
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# (Optional) seed embeddings if missing:
python scripts/build_embeddings.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
**Web**
```bash
cd web
npm ci
npm run dev
```

## Seeding embeddings
If `api/data/embeddings.npz` is missing or you change `words.txt`, build:
```bash
cd api
python scripts/build_embeddings.py
```
This downloads the model on first run (CPU-only).

## Configuration
Create `api/.env` from the example:
```env
MONGO_URL=mongodb://localhost:27017/word-detective-lite
DAILY_SEED_SALT=change-me
CORS_ORIGINS=http://localhost:5173
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

## API Reference
### `GET /api/health`
**Response**
```json
{ "ok": true }
```

### `POST /api/game`
Body:
```json
{ "mode": "daily" }
```
or
```json
{ "mode": "free" }
```
Response:
```json
{ "gameId": "64...", "mode": "daily", "startedAt": "2025-09-15T09:00:00Z" }
```

### `POST /api/guess`
Body:
```json
{ "gameId": "64...", "word": "banana" }
```
Response:
```json
{
  "normalizedWord": "banana",
  "similarity": 0.62,
  "band": "Warm",
  "attempts": 3,
  "isCorrect": false
}
```

Errors (4xx):
```json
{ "error": { "code": "OOV", "message": "word not in vocabulary" } }
```

### `GET /api/game/{id}`
Response (example):
```json
{
  "gameId": "64...",
  "mode": "daily",
  "startedAt": "2025-09-15T09:00:00Z",
  "attempts": 3,
  "lastGuesses": [
    { "normalizedWord": "apple", "similarity": 0.18, "band": "Cold", "isCorrect": false, "at": "2025-09-15T09:02:01Z" },
    { "normalizedWord": "grape", "similarity": 0.42, "band": "Cool", "isCorrect": false, "at": "2025-09-15T09:01:21Z" }
  ]
}
```

## Data Model
**games**
```json
{ "_id": "...", "sessionId": "...", "mode": "daily", "targetIndex": 123, "startedAt": "...", "completedAt": null, "attempts": 3, "dailyDate": "2025-09-15" }
```
**guesses**
```json
{ "_id": "...", "gameId": "...", "sessionId": "...", "word": "banana", "normalizedWord": "banana", "similarity": 0.62, "band": "Warm", "isCorrect": false, "createdAt": "..." }
```

## Testing
```bash
cd api
pytest -q
```
Covers normalization, band thresholds (exact boundaries), daily seed determinism, and API happy path.

## Accessibility
- Input remains focused; Enter submits
- Feedback announced via ARIA live region
- Color legend includes text labels

## Troubleshooting
- First run may download the embedding model; this can take a little while on CPU.
- Ensure MongoDB is running (Docker Compose includes it).
- If CORS errors occur, set `CORS_ORIGINS` to the exact web origin (e.g., `http://localhost:5173`).

## Roadmap
- Trend chart polish
- Simple daily leaderboard
- Optional themed word packs

## License
MIT
