from backend.src.models.users import create_user, get_user_by_id, get_user_by_email, delete_user


def test_create_user():
    """Test creating a user."""
    name = "Test User"
    email = "test@gmail.com"
    password_hash = "dsjfljio13efd"
    user_id = create_user(name, email, password_hash)
    assert user_id is not None, "User creation failed"

    user = get_user_by_id(user_id)
    assert user is not None, "User not found after creation"
    assert user['user_id'] == user_id, "User ID does not match"

    user = get_user_by_email(email)
    assert user is not None, "User not found by email"
    assert user['user_id'] == user_id, "User ID does not match"

    assert delete_user(user_id) == True, "User deletion failed"
    assert get_user_by_id(user_id) is None, "User still exists after deletion"



