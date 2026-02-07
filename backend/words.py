import random
from pathlib import Path

_valid_words: dict[int, set[str]] = {}
_target_words: dict[int, list[str]] = {}

def _load(length: int) -> None:
    if length in _valid_words:
        return
    path = Path(__file__).parent / f"words_{length}.txt"
    words = set(path.read_text().strip().split("\n"))
    _valid_words[length] = words
    _target_words[length] = [w for w in words if not w.endswith('s')]

def is_valid_word(word: str, length: int) -> bool:
    _load(length)
    return word.lower() in _valid_words[length]

def get_random_target(length: int) -> str:
    _load(length)
    return random.choice(_target_words[length])
