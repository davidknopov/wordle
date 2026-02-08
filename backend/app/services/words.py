import random
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent.parent / "data"

@lru_cache(maxsize=4)
def _load_words(length: int) -> tuple[set[str], list[str]]:
    """
    Load and cache word list for a given length.
    
    Returns:
        Tuple of (all valid words set, non-plural target words list)
    """
    path = DATA_DIR / f"words_{length}.txt"
    words = set(path.read_text().strip().split("\n"))
    targets = [w for w in words if not w.endswith('s')]
    return words, targets

def is_valid_word(word: str, length: int) -> bool:
    """Check if a word is valid for the given length."""
    valid_words, _ = _load_words(length)
    return word.lower() in valid_words

def get_random_target(length: int) -> str:
    """Get a random non-plural target word of the given length."""
    _, targets = _load_words(length)
    return random.choice(targets)
