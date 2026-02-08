from app.models.game import LetterFeedback, LetterStatus

def compute_feedback(guess: str, target: str) -> list[LetterFeedback]:
    """
    Compute Wordle feedback for a guess against a target word.
    
    Uses two-pass algorithm to correctly handle duplicate letters:
    1. First pass: Mark exact matches (green/correct)
    2. Second pass: Mark present (yellow) or absent (gray)
    
    Args:
        guess: The guessed word
        target: The target word to match against
        
    Returns:
        List of LetterFeedback for each position
    """
    guess = guess.lower()
    target = target.lower()
    n = len(target)
    result: list[LetterFeedback | None] = [None] * n
    remaining = list(target)

    # Pass 1: Mark exact matches (green)
    for i in range(n):
        if guess[i] == target[i]:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.CORRECT)
            remaining[i] = None

    # Pass 2: Mark present (yellow) or absent (gray)
    for i in range(n):
        if result[i] is not None:
            continue
        if guess[i] in remaining:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.PRESENT)
            remaining[remaining.index(guess[i])] = None
        else:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.ABSENT)

    return result
