import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None
games = None
guesses = None

async def init_db():
    global client, db, games, guesses
    url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/word-detective-lite')
    client = AsyncIOMotorClient(url)
    db = client.get_default_database() if '/' in url.split('//',1)[-1] else client['word-detective-lite']
    games = db['games']
    guesses = db['guesses']
    # Indexes
    await games.create_index('sessionId')
    await guesses.create_index([('gameId',1),('createdAt',1)])
