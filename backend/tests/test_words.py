import pytest
from app.services.words import is_valid_word, get_random_target


class TestIsValidWord:
    def test_valid_5_letter_word(self):
        assert is_valid_word('crane', 5) is True
    
    def test_invalid_5_letter_word(self):
        assert is_valid_word('xyzab', 5) is False
    
    def test_valid_6_letter_word(self):
        assert is_valid_word('planet', 6) is True
    
    def test_case_insensitive(self):
        assert is_valid_word('CRANE', 5) is True
        assert is_valid_word('CrAnE', 5) is True


class TestGetRandomTarget:
    def test_returns_correct_length(self):
        for length in [5, 6, 7, 8]:
            word = get_random_target(length)
            assert len(word) == length
    
    def test_returns_non_plural(self):
        for _ in range(20):
            word = get_random_target(5)
            assert not word.endswith('s'), f"Got plural word: {word}"
    
    def test_returns_valid_word(self):
        for length in [5, 6, 7, 8]:
            word = get_random_target(length)
            assert is_valid_word(word, length)
