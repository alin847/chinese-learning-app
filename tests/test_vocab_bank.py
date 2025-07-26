from backend.src.models.vocab_bank import add_vocab, add_vocab_batch, update_vocab, get_vocab, get_all_vocab, delete_vocab, get_random_vocab, get_random_practice
from backend.src.models.users import create_user, delete_user
from datetime import date, timedelta
import pytest

def test_vocab():
    name = "Test User"
    email = "test@gmail.com"
    password_hash = "dsjfljio13efd"
    user_id = create_user(name, email, password_hash)

    # Test adding a vocabulary word
    simplified_id = 147101
    assert add_vocab(user_id, simplified_id) is True, "Adding a valid vocabulary word should return an ID"

    # Test no duplicate vocabulary word
    try:
        add_vocab(user_id, simplified_id)
        pytest.fail("Adding a duplicate vocabulary word should raise an Exception")
    except Exception as e:
        # If exception is raised, test passes; optionally, you can check the exception message here
        pass

    # Test retrieving the vocabulary word
    vocab = get_vocab(user_id, simplified_id)
    vocab_bank_id = vocab["vocab_bank_id"]
    assert vocab["simplified_id"] == simplified_id, "Simplified ID does not match"
    assert vocab["repetitions"] == 0, "Repetitions should be 0 for a new word"
    assert vocab["interval"] == 0, "Interval should be 0 for a new word"
    assert vocab["ease_factor"] == 2.5, "Ease factor should be 2.5 for a new word"
    assert vocab["last_reviewed"] is None, "Last reviewed should be None for a new word"
    assert vocab["next_review"] == date.today(), "Next review should be today's date for a new word"

    # Test updating the vocabulary word
    update_data = {
        "simplified_id": simplified_id,
        "repetitions": 1,
        "interval": 1,
        "ease_factor": 2.5}
    assert update_vocab(user_id, update_data) is True, "Updating vocabulary word failed"

    # Test retrieving the updated vocabulary word
    updated_vocab = get_vocab(user_id, simplified_id)
    assert updated_vocab["vocab_bank_id"] == vocab_bank_id, "Vocab bank ID should remain the same after update"
    assert updated_vocab["repetitions"] == 1, "Repetitions were not updated correctly"
    assert updated_vocab["interval"] == 1, "Interval was not updated correctly"
    assert updated_vocab["ease_factor"] == 2.5, "Ease factor was not updated correctly"
    assert updated_vocab["last_reviewed"] == date.today(), "Last reviewed date was not updated correctly"
    assert updated_vocab["next_review"] == date.today() + timedelta(days=1), "Next review date was not updated correctly"

    # Testing adding a batch of vocabulary words
    simplified_ids = [109899, 144778, 94164]
    repetitions = [0, 0, 0]
    intervals = [0, 0, 0]
    next_review = [date.today(), date.today(), date.today()]
    assert add_vocab_batch(user_id, simplified_ids, repetitions, intervals, next_review) is True, "Adding a batch of vocabulary words failed"

    # Test retrieving all vocabulary words
    all_vocab = get_all_vocab(user_id)
    assert len(all_vocab) == 4, "There should be four vocabulary word in the bank"


    # Test deleting the vocabulary word
    assert delete_vocab(user_id, simplified_id) is True, "Deleting vocabulary word failed"
    assert get_vocab(user_id, simplified_id) is None, "Vocabulary word should be deleted"
    
    # Test deleting a non-existent vocabulary word
    assert delete_vocab(user_id, simplified_id) is True, "Deleting a non-existent vocabulary word should return True"
    
    # Test getting random vocabulary word (kinda hard to test)
    random_vocab = get_random_vocab(user_id, limit=1)
    assert len(random_vocab) == 1, "Should return one random vocabulary word"

    # Test getting random practice vocabulary words
    random_practice = get_random_practice(user_id, limit=1)
    assert len(random_practice) == 1, "Should return one random practice vocabulary words"  
    assert random_practice[0]["simplified_id"] in simplified_ids, "Random practice word should be one of the batch added words"

    # Clean up
    delete_user(user_id)
