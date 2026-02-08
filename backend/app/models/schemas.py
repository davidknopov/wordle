from pydantic import BaseModel, Field
from app.models.game import Guess, GameStatus

# Request schemas
class CreateGameRequest(BaseModel):
    word_length: int = Field(ge=5, le=8)

class SubmitGuessRequest(BaseModel):
    word: str

# Response schemas
class CreateGameResponse(BaseModel):
    id: str
    word_length: int
    max_guesses: int
    status: GameStatus

class SubmitGuessResponse(BaseModel):
    word: str
    feedback: list
    game_status: GameStatus
    guesses_remaining: int

class GameStateResponse(BaseModel):
    id: str
    word_length: int
    max_guesses: int
    status: GameStatus
    guesses: list[Guess]
    guesses_remaining: int
    target_word: str | None
