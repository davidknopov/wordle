from game import Game

class GameStore:
    def __init__(self):
        self._games: dict[str, Game] = {}

    def save(self, game: Game) -> None:
        self._games[game.id] = game

    def get(self, game_id: str) -> Game | None:
        return self._games.get(game_id)

store = GameStore()
