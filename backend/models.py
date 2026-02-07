from pydantic import BaseModel, Field
from enum import Enum

class LetterStatus(str, Enum):
    CORRECT = "correct"   # green
    PRESENT = "present"   # yellow
    ABSENT = "absent"     # gray

class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

class LetterFeedback(BaseModel):
    letter: str
    status: LetterStatus

class Guess(BaseModel):
    word: str
    feedback: list[LetterFeedback]

class CreateGameRequest(BaseModel):
    word_length: int = Field(ge=5, le=8)

class CreateGameResponse(BaseModel):
    id: str
    word_length: int
    max_guesses: int
    status: GameStatus

class SubmitGuessRequest(BaseModel):
    word: str

class SubmitGuessResponse(BaseModel):
    word: str
    feedback: list[LetterFeedback]
    game_status: GameStatus
    guesses_remaining: int

class GameStateResponse(BaseModel):
    id: str
    word_length: int
    max_guesses: int
    status: GameStatus
    guesses: list[Guess]
    guesses_remaining: int
    target_word: str | None  # revealed only when game over
