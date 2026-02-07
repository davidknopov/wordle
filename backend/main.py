import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    CreateGameRequest, CreateGameResponse, SubmitGuessRequest, 
    SubmitGuessResponse, GameStateResponse, Guess, GameStatus
)
from game import Game
from store import store
from words import is_valid_word, get_random_target
from feedback import compute_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/games", response_model=CreateGameResponse)
def create_game(req: CreateGameRequest):
    game = Game(
        id=str(uuid.uuid4()),
        word_length=req.word_length,
        target_word=get_random_target(req.word_length),
    )
    store.save(game)
    return CreateGameResponse(
        id=game.id,
        word_length=game.word_length,
        max_guesses=game.max_guesses,
        status=game.status,
    )

@app.post("/games/{game_id}/guesses", response_model=SubmitGuessResponse)
def submit_guess(game_id: str, req: SubmitGuessRequest):
    game = store.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    word = req.word.lower()
    
    if len(word) != game.word_length:
        raise HTTPException(status_code=400, detail=f"Word must be {game.word_length} letters")
    
    if not is_valid_word(word, game.word_length):
        raise HTTPException(status_code=400, detail="Not a valid word")
    
    feedback = compute_feedback(word, game.target_word)
    guess = Guess(word=word, feedback=feedback)
    game.guesses.append(guess)
    
    if word == game.target_word.lower():
        game.status = GameStatus.WON
    elif game.guesses_remaining == 0:
        game.status = GameStatus.LOST
    
    store.save(game)
    
    return SubmitGuessResponse(
        word=word,
        feedback=feedback,
        game_status=game.status,
        guesses_remaining=game.guesses_remaining,
    )

@app.get("/games/{game_id}", response_model=GameStateResponse)
def get_game(game_id: str):
    game = store.get(game_id)
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
