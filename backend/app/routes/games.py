import uuid
from fastapi import APIRouter, HTTPException

from app.models import (
    CreateGameRequest, CreateGameResponse,
    SubmitGuessRequest, SubmitGuessResponse,
    GameStateResponse, Guess, GameStatus
)
from app.services import (
    Game, game_repository,
    is_valid_word, get_random_target, compute_feedback
)

router = APIRouter(prefix="/games", tags=["games"])


@router.post("", response_model=CreateGameResponse)
def create_game(req: CreateGameRequest):
    """Create a new Wordle game with the specified word length."""
    game = Game(
        id=str(uuid.uuid4()),
        word_length=req.word_length,
        target_word=get_random_target(req.word_length),
    )
    game_repository.save(game)
    return CreateGameResponse(
        id=game.id,
        word_length=game.word_length,
        max_guesses=game.max_guesses,
        status=game.status,
    )


@router.post("/{game_id}/guesses", response_model=SubmitGuessResponse)
def submit_guess(game_id: str, req: SubmitGuessRequest):
    """Submit a guess for an existing game."""
    game = game_repository.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    word = req.word.lower()
    
    if len(word) != game.word_length:
        raise HTTPException(
            status_code=400, 
            detail=f"Word must be {game.word_length} letters"
        )
    
    if not is_valid_word(word, game.word_length):
        raise HTTPException(status_code=400, detail="Not a valid word")
    
    feedback = compute_feedback(word, game.target_word)
    guess = Guess(word=word, feedback=feedback)
    game.guesses.append(guess)
    
    # Check win/lose conditions
    if word == game.target_word.lower():
        game.status = GameStatus.WON
    elif game.guesses_remaining == 0:
        game.status = GameStatus.LOST
    
    game_repository.save(game)
    
    return SubmitGuessResponse(
        word=word,
        feedback=feedback,
        game_status=game.status,
        guesses_remaining=game.guesses_remaining,
    )


@router.get("/{game_id}", response_model=GameStateResponse)
def get_game(game_id: str):
    """Retrieve the current state of a game."""
    game = game_repository.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameStateResponse(
        id=game.id,
        word_length=game.word_length,
        max_guesses=game.max_guesses,
        status=game.status,
        guesses=game.guesses,
        guesses_remaining=game.guesses_remaining,
        target_word=game.target_word if game.status != GameStatus.IN_PROGRESS else None,
    )
