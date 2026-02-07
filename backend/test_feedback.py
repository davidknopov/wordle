import pytest
from feedback import compute_feedback
from models import LetterStatus

def status_string(feedback):
    """Convert feedback to string like 'CPPAA' for easy assertion"""
    return ''.join(f.status.value[0].upper() for f in feedback)

class TestFeedbackBasic:
    def test_all_correct(self):
        fb = compute_feedback('crane', 'crane')
        assert status_string(fb) == 'CCCCC'
    
    def test_all_absent(self):
        fb = compute_feedback('xxxxx', 'crane')
        assert status_string(fb) == 'AAAAA'
    
    def test_mixed_feedback(self):
        fb = compute_feedback('crane', 'apple')
        # c=absent, r=absent, a=present, n=absent, e=correct (e is in position 5 in both)
        assert status_string(fb) == 'AAPAC'

class TestFeedbackDuplicateLetters:
    """Critical: duplicate letter handling is where most implementations fail"""
    
    def test_guess_has_duplicate_target_has_one(self):
        # Guess 'hello' has 2 Ls, target 'world' has 1 L at position 4
        fb = compute_feedback('hello', 'world')
        # h=absent, e=absent, l=absent (not at pos 3), l=correct (at pos 4), o=present
        assert status_string(fb) == 'AAACP'
    
    def test_target_has_duplicate_guess_has_one(self):
        # Target 'apple' has 2 Ps, guess 'paper' has 2 Ps
        fb = compute_feedback('paper', 'apple')
        # p=present, a=present, p=correct, e=present, r=absent
        assert status_string(fb) == 'PPCPA'
    
    def test_one_correct_one_absent_same_letter(self):
        # Guess 'speed' vs target 'abide'
        fb = compute_feedback('speed', 'abide')
        # s=absent, p=absent, e=present, e=absent (only one e), d=present
        assert status_string(fb) == 'AAPAP'
    
    def test_correct_takes_priority_over_present(self):
        # Guess 'creep' vs target 'sheep'
        fb = compute_feedback('creep', 'sheep')
        # c=absent, r=absent, e=correct, e=correct, p=correct
        assert status_string(fb) == 'AACCC'
    
    def test_triple_letter_in_guess(self):
        # Guess 'geese' vs target 'eagle'
        fb = compute_feedback('geese', 'eagle')
        # g=present, e=present, e=absent (2 e's in target, one used for correct), s=absent, e=correct
        assert status_string(fb) == 'PPAAC'
    
    def test_anagram(self):
        # All letters present but none in right position
        fb = compute_feedback('nrace', 'crane')
        # n=present, r=correct, a=correct, c=present, e=correct
        assert status_string(fb) == 'PCCPC'

class TestFeedbackEdgeCases:
    def test_case_insensitive(self):
        fb = compute_feedback('CRANE', 'crane')
        assert status_string(fb) == 'CCCCC'
    
    def test_different_lengths_6(self):
        fb = compute_feedback('planet', 'planet')
        assert status_string(fb) == 'CCCCCC'
    
    def test_different_lengths_8(self):
        fb = compute_feedback('absolute', 'absolute')
        assert status_string(fb) == 'CCCCCCCC'
