from pydantic import BaseModel, Field
from enum import Enum

class LetterStatus(str, Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"

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
