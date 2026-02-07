from models import LetterFeedback, LetterStatus

def compute_feedback(guess: str, target: str) -> list[LetterFeedback]:
    guess = guess.lower()
    target = target.lower()
    n = len(target)
    result = [None] * n
    remaining = list(target)

    # First pass: mark correct (green)
    for i in range(n):
        if guess[i] == target[i]:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.CORRECT)
            remaining[i] = None

    # Second pass: mark present (yellow) or absent (gray)
    for i in range(n):
        if result[i] is not None:
            continue
        if guess[i] in remaining:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.PRESENT)
            remaining[remaining.index(guess[i])] = None
        else:
            result[i] = LetterFeedback(letter=guess[i], status=LetterStatus.ABSENT)

    return result
