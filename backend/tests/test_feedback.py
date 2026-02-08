import pytest
from app.services.feedback import compute_feedback
from app.models.game import LetterStatus


class TestFeedbackBasic:
    def test_all_correct(self):
        feedback = compute_feedback('apple', 'apple')
        assert all(f.status == LetterStatus.CORRECT for f in feedback)
    
    def test_all_absent(self):
        feedback = compute_feedback('brick', 'mound')
        assert all(f.status == LetterStatus.ABSENT for f in feedback)
    
    def test_mixed_feedback(self):
        feedback = compute_feedback('crane', 'react')
        statuses = [f.status for f in feedback]
        assert statuses[0] == LetterStatus.PRESENT  # c in react
        assert statuses[1] == LetterStatus.PRESENT  # r in react
        assert statuses[2] == LetterStatus.CORRECT  # a in position 2 of react
        assert statuses[3] == LetterStatus.ABSENT   # n not in react
        assert statuses[4] == LetterStatus.PRESENT  # e in react


class TestFeedbackDuplicates:
    def test_duplicate_one_correct_one_absent(self):
        # guess 'speed' against 'creep': two e's in guess, two in target
        feedback = compute_feedback('speed', 'creep')
        statuses = [f.status for f in feedback]
        assert statuses[2] == LetterStatus.CORRECT  # first e correct
        assert statuses[3] == LetterStatus.CORRECT  # second e correct
    
    def test_duplicate_letter_limited_by_target(self):
        # guess 'geese' against 'creep': three e's in guess, two in target
        feedback = compute_feedback('geese', 'creep')
        statuses = [f.status for f in feedback]
        e_statuses = [statuses[1], statuses[2], statuses[4]]
        correct_count = sum(1 for s in e_statuses if s == LetterStatus.CORRECT)
        present_count = sum(1 for s in e_statuses if s == LetterStatus.PRESENT)
        absent_count = sum(1 for s in e_statuses if s == LetterStatus.ABSENT)
        assert correct_count + present_count == 2
        assert absent_count == 1
    
    def test_correct_takes_priority(self):
        # guess 'speed' against 'creep': e at positions 2,3 match creep positions 2,3
        feedback = compute_feedback('speed', 'creep')
        assert feedback[2].status == LetterStatus.CORRECT  # e matches e
        assert feedback[3].status == LetterStatus.CORRECT  # e matches e


class TestFeedbackCaseInsensitive:
    def test_uppercase_guess(self):
        feedback = compute_feedback('APPLE', 'apple')
        assert all(f.status == LetterStatus.CORRECT for f in feedback)
    
    def test_mixed_case(self):
        feedback = compute_feedback('ApPlE', 'APPLE')
        assert all(f.status == LetterStatus.CORRECT for f in feedback)
