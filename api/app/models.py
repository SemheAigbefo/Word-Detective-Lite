from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class ErrorShape(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    error: ErrorShape

class CreateGameRequest(BaseModel):
    mode: Literal['daily','free']

class CreateGameResponse(BaseModel):
    gameId: str
    mode: str
    startedAt: str

class GuessRequest(BaseModel):
    gameId: str
    word: str

class GuessResponse(BaseModel):
    normalizedWord: str
    similarity: float
    band: Literal['Cold','Cool','Warm','Hot','Very Hot']
    attempts: int
    isCorrect: bool

class GuessPublic(BaseModel):
    normalizedWord: str
    similarity: float
    band: Literal['Cold','Cool','Warm','Hot','Very Hot']
    isCorrect: bool
    at: str

class GameState(BaseModel):
    gameId: str
    mode: str
    startedAt: str
    attempts: int
    lastGuesses: List[GuessPublic] = Field(default_factory=list)
