from backend.src.models.test_bank import get_random_question

def test_get_random_question():
    # Test 1: Get a random question at each level with no exclusions
    for level in range(1, 7):
        excluded = []
        question = get_random_question(level, excluded)
        assert question, f"Should return a question for level {level}"
        assert question['question_id'] in set(range(601+50*(level-1), 651+50*(level-1))), f"Question level should match requested level {level}"

    # Test 2: Get a random question at level 1 with exclusions
    level = 1
    excluded = list(range(601, 650))
    question = get_random_question(level, excluded)
    assert question, "Should return a question for level 1"
    assert question['question_id'] == 650, "Question ID should not be in the excluded list"

    # Test 3: Get a random question with no questions available
    excluded = list(range(601, 651))
    question = get_random_question(level, excluded)
    assert not question, "Should return an empty dictionary if no questions are available"