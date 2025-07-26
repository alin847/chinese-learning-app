from backend.src.models.progress import get_progress, add_practice_completed, add_time_spent
from backend.src.models.users import create_user, delete_user

def test_progress():
    # create a test user
    name = "Test User"
    email = "test@gmail.com"
    password_hash = "dsjfljio13efd"
    user_id = create_user(name, email, password_hash)

    # get initial progress
    progress = get_progress(user_id)
    assert progress['learning_count'] == 0, "Initial learning count should be 0"
    assert progress['reviewing_count'] == 0, "Initial reviewing count should be 0"
    assert progress['mastered_count'] == 0, "Initial mastered count should be 0"
    assert progress['time_spent'] == 0, "Initial time spent should be 0"
    assert progress['practice_completed'] == 0, "Initial practice completed should be 0"

    # add time spent
    time_spent = 120  # in seconds
    assert add_time_spent(user_id, time_spent) is True, "Adding time spent should return True"

    # add practice completed
    assert add_practice_completed(user_id) is True, "Adding practice completed should return True"

    # get updated progress
    updated_progress = get_progress(user_id)
    assert updated_progress['time_spent'] == time_spent, "Time spent should match the added time"
    assert updated_progress['practice_completed'] == 1, "Practice completed should be incremented by 1"

    # clean up by deleting the test user
    delete_user(user_id)
