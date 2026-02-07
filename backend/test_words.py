import pytest
from words import is_valid_word, get_random_target

class TestWordValidation:
    def test_valid_5_letter_word(self):
        assert is_valid_word('crane', 5) is True
    
    def test_invalid_5_letter_word(self):
        assert is_valid_word('xyzab', 5) is False
    
    def test_valid_6_letter_word(self):
        assert is_valid_word('planet', 6) is True
    
    def test_case_insensitive(self):
        assert is_valid_word('CRANE', 5) is True
        assert is_valid_word('CrAnE', 5) is True

class TestRandomTarget:
    def test_returns_correct_length_5(self):
        word = get_random_target(5)
        assert len(word) == 5
    
    def test_returns_correct_length_6(self):
        word = get_random_target(6)
        assert len(word) == 6
    
    def test_returns_correct_length_7(self):
        word = get_random_target(7)
        assert len(word) == 7
    
    def test_returns_correct_length_8(self):
        word = get_random_target(8)
        assert len(word) == 8
    
    def test_target_not_plural(self):
        # Run multiple times to increase confidence
        for _ in range(100):
            word = get_random_target(5)
            assert not word.endswith('s'), f"Target '{word}' is plural"
    
    def test_target_is_valid_word(self):
        for length in [5, 6, 7, 8]:
            word = get_random_target(length)
            assert is_valid_word(word, length)
