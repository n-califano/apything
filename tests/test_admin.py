def test_get_users(api_client):
    # Setup
    user_id = api_client.admin.create_user(username="test_user", password="p4ssw0rd", role='default')
    
    users = api_client.admin.get_users()
    
    assert len(users) != 0
    assert any(user.username == "test_user" and user.role == 'default' for user in users)

    # Teardown
    api_client.admin.remove_user(user_id=user_id)

def test_create_user(api_client):
    user_id = api_client.admin.create_user(username="test_user", password="p4ssw0rd", role='default')
    users = api_client.admin.get_users()

    assert isinstance(user_id, int)
    assert user_id > 0
    assert any(user.username == "test_user" and user.role == 'default' for user in users)

    manager_id = api_client.admin.create_user(username="test_manager", password="m4n4g3r!!", role='manager')
    users = api_client.admin.get_users()

    assert isinstance(manager_id, int)
    assert manager_id > 0
    assert any(user.username == "test_manager" and user.role == 'manager' for user in users)

    admin_id = api_client.admin.create_user(username="test_admin", password="adminadmin", role='admin')
    users = api_client.admin.get_users()

    assert isinstance(admin_id, int)
    assert admin_id > 0
    assert any(user.username == "test_admin" and user.role == 'admin' for user in users)

    # Teardown
    api_client.admin.remove_user(user_id=user_id)
    api_client.admin.remove_user(user_id=manager_id)
    api_client.admin.remove_user(user_id=admin_id)


def test_remove_user(api_client):
    # Setup
    user_id = api_client.admin.create_user(username="test_user", password="p4ssw0rd", role='default')

    is_success = api_client.admin.remove_user(user_id=user_id)
    users = api_client.admin.get_users()

    assert is_success is True
    assert not any(user.username == "test_user" and user.role == 'default' for user in users)