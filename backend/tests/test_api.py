import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCreateGame:
    def test_create_game_5_letters(self):
        res = client.post('/games', json={'word_length': 5})
        assert res.status_code == 200
        data = res.json()
        assert data['word_length'] == 5
        assert data['max_guesses'] == 6
        assert data['status'] == 'in_progress'
        assert 'id' in data
    
    def test_create_game_8_letters(self):
        res = client.post('/games', json={'word_length': 8})
        assert res.status_code == 200
        data = res.json()
        assert data['word_length'] == 8
        assert data['max_guesses'] == 9
    
    def test_create_game_invalid_length_too_short(self):
        res = client.post('/games', json={'word_length': 4})
        assert res.status_code == 422
    
    def test_create_game_invalid_length_too_long(self):
        res = client.post('/games', json={'word_length': 9})
        assert res.status_code == 422


class TestSubmitGuess:
    def test_submit_valid_guess(self):
        game = client.post('/games', json={'word_length': 5}).json()
        res = client.post(f"/games/{game['id']}/guesses", json={'word': 'crane'})
        assert res.status_code == 200
        data = res.json()
        assert data['word'] == 'crane'
        assert len(data['feedback']) == 5
        assert data['guesses_remaining'] == 5
    
    def test_submit_invalid_word(self):
        game = client.post('/games', json={'word_length': 5}).json()
        res = client.post(f"/games/{game['id']}/guesses", json={'word': 'xyzab'})
        assert res.status_code == 400
        assert 'Not a valid word' in res.json()['detail']
    
    def test_submit_wrong_length(self):
        game = client.post('/games', json={'word_length': 5}).json()
        res = client.post(f"/games/{game['id']}/guesses", json={'word': 'planets'})
        assert res.status_code == 400
        assert 'must be 5 letters' in res.json()['detail']
    
    def test_game_not_found(self):
        res = client.post('/games/nonexistent-id/guesses', json={'word': 'crane'})
        assert res.status_code == 404


class TestGetGame:
    def test_get_game_state(self):
        game = client.post('/games', json={'word_length': 5}).json()
        client.post(f"/games/{game['id']}/guesses", json={'word': 'crane'})
        
        res = client.get(f"/games/{game['id']}")
        assert res.status_code == 200
        data = res.json()
        assert len(data['guesses']) == 1
        assert data['guesses'][0]['word'] == 'crane'
        assert data['target_word'] is None
    
    def test_target_revealed_on_loss(self):
        game = client.post('/games', json={'word_length': 5}).json()
        words = ['crane', 'slate', 'audio', 'piano', 'about', 'youth']
        for word in words:
            client.post(f"/games/{game['id']}/guesses", json={'word': word})
        
        res = client.get(f"/games/{game['id']}")
        data = res.json()
        assert data['status'] == 'lost'
        assert data['target_word'] is not None
    
    def test_game_not_found(self):
        res = client.get('/games/nonexistent-id')
        assert res.status_code == 404


class TestGameFlow:
    def test_cannot_guess_after_game_over(self):
        game = client.post('/games', json={'word_length': 5}).json()
        words = ['crane', 'slate', 'audio', 'piano', 'about', 'youth']
        for word in words:
            client.post(f"/games/{game['id']}/guesses", json={'word': word})
        
        res = client.post(f"/games/{game['id']}/guesses", json={'word': 'extra'})
        assert res.status_code == 400
        assert 'already over' in res.json()['detail']
