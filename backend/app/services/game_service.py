from dataclasses import dataclass, field
from typing import Protocol
from app.models import Guess, GameStatus

@dataclass
class Game:
    """Domain entity representing a Wordle game."""
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


class GameRepository(Protocol):
    """Interface for game persistence."""
    def save(self, game: Game) -> None: ...
    def get(self, game_id: str) -> Game | None: ...


class InMemoryGameRepository:
    """In-memory implementation of GameRepository."""
    
    def __init__(self):
        self._games: dict[str, Game] = {}

    def save(self, game: Game) -> None:
        self._games[game.id] = game

    def get(self, game_id: str) -> Game | None:
        return self._games.get(game_id)


# Singleton instance
game_repository = InMemoryGameRepository()
