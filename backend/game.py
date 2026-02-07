from dataclasses import dataclass, field
from models import Guess, GameStatus

@dataclass
class Game:
    id: str
    word_length: int
    target_word: str
    guesses: list[Guess] = field(default_factory=list)
    status: GameStatus = GameStatus.IN_PROGRESS

    @property
    def max_guesses(self) -> int:
        return self.word_length + 1

    @property
    def guesses_remaining(self) -> int:
        return self.max_guesses - len(self.guesses)
