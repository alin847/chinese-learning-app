from backend.models.vocab_bank import add_vocab, update_vocab, get_vocab, get_all_vocab, delete_vocab
from backend.models.users import create_user, delete_user
from datetime import date, timedelta

# add more robust test cases later
# need to fix
def test_vocab():
    email = "test@gmail.com"
    password_hash = "dsjfljio13efd"
    user_id = create_user(email, password_hash)

    # Test adding a nonexistent vocabulary word
    simplified_id = 1
    simplified = "测试"
    vocab_id = add_vocab(user_id, simplified_id, simplified)
    assert vocab_id is None, "Adding a nonexistent vocabulary word should return None"

    # Test adding a valid vocabulary word
    simplified_id = 147101
    simplified = "海星"
    vocab_id = add_vocab(user_id, simplified_id, simplified)
    assert vocab_id is not None, "Adding a valid vocabulary word should return an ID"


    # Test retrieving the vocabulary word
    vocab = get_vocab(user_id, simplified_id)
    assert vocab["id"] == vocab_id, "Retrieved vocabulary word does not match added word"
    assert vocab["simplified_id"] == simplified_id, "Simplified ID does not match"
    assert vocab["simplified"] == simplified, "Simplified word does not match"
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
    assert updated_vocab["repetitions"] == 1, "Repetitions were not updated correctly"
    assert updated_vocab["interval"] == 1, "Interval was not updated correctly"
    assert updated_vocab["ease_factor"] == 2.5, "Ease factor was not updated correctly"
    assert updated_vocab["last_reviewed"] == date.today(), "Last reviewed date was not updated correctly"
    assert updated_vocab["next_review"] == date.today() + timedelta(days=1), "Next review date was not updated correctly"

    # Test retrieving all vocabulary words
    all_vocab = get_all_vocab(user_id)
    assert len(all_vocab) == 1, "There should be one vocabulary word in the bank"
    assert all_vocab[0]["id"] == vocab_id, "Retrieved vocabulary word ID does not match added word ID"

    # Clean up
    assert delete_vocab(user_id, simplified_id) is True, "Deleting vocabulary word failed"
    assert get_vocab(user_id, simplified_id) is None, "Vocabulary word should be deleted"
    delete_user(user_id)
