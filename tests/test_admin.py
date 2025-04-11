import pytest
from apything import ApythingRequestException


@pytest.fixture
def test_user(api_client):
    # Setup
    username = 'test_user'
    role = 'default'
    id = api_client.admin.create_user(username=username, password="p4ssw0rd", role=role)
    yield username, role, id
    # Teardown
    api_client.admin.remove_user(id)

@pytest.fixture
def test_user2(api_client):
    # Setup
    username = 'test_user2'
    role = 'manager'
    id = api_client.admin.create_user(username=username, password="p4ssw0rd", role=role)
    yield username, role, id
    # Teardown
    api_client.admin.remove_user(id)

@pytest.fixture
def test_user3(api_client):
    # Setup
    username = 'test_user3'
    role = 'admin'
    id = api_client.admin.create_user(username=username, password="p4ssw0rd", role=role)
    yield username, role, id
    # Teardown
    api_client.admin.remove_user(id)


def test_get_users(api_client, test_user):   # Need to pass test_user to make sure the fixture run, even if var is not actually used 
    test_user_name, test_user_role, _ = test_user
    users = api_client.admin.get_users()
    
    assert len(users) != 0
    assert any(user.username == test_user_name and user.role == test_user_role for user in users)


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
    user_id = api_client.admin.create_user(username="test_remove_user", password="p4ssw0rd", role='default')

    is_success = api_client.admin.remove_user(user_id=user_id)
    users = api_client.admin.get_users()

    assert is_success is True
    assert not any(user.username == "test_remove_user" and user.role == 'default' for user in users)

def test_assign_workspace_to_users(api_client, test_workspace, test_user, test_user2, test_user3):
    _, role, id = test_user

    is_success = api_client.admin.assign_workspace_to_users(workspace_slug=test_workspace.slug, user_ids=[id])
    allowed_users = api_client.admin.get_allowed_users_for_workspace(workspace_id=test_workspace.id)

    assert is_success is True
    assert len(allowed_users) == 1
    assert (id, role) in allowed_users

    _, role2, id2 = test_user2
    _, role3, id3 = test_user3
    is_success = api_client.admin.assign_workspace_to_users(workspace_slug=test_workspace.slug, user_ids=[id2, id3], reset=True)
    allowed_users = api_client.admin.get_allowed_users_for_workspace(workspace_id=test_workspace.id)
    
    assert is_success is True
    assert len(allowed_users) == 2
    assert (id, role) not in allowed_users
    assert (id2, role2) in allowed_users
    assert (id3, role3) in allowed_users


def test_get_allowed_users_for_workspace(api_client, test_workspace, test_user, test_user2, test_user3):
    # Setup
    _, role, id = test_user
    _, role2, id2 = test_user2
    _, role3, id3 = test_user3
    api_client.admin.assign_workspace_to_users(workspace_slug=test_workspace.slug, user_ids=[id, id2, id3])

    allowed_users = api_client.admin.get_allowed_users_for_workspace(workspace_id=test_workspace.id)

    assert len(allowed_users) == 3
    assert (id, role) in allowed_users
    assert (id2, role2) in allowed_users
    assert (id3, role3) in allowed_users


def test_update_user_with_all_params(api_client, test_user):
    _, _, user_id = test_user

    is_success = api_client.admin.update_user(user_id=user_id, new_username="updated_username", new_password='new password', new_role='admin', is_suspended=True)

    users = api_client.admin.get_users()

    assert is_success is True
    assert any(user.username == "updated_username" and user.role == 'admin' and user.suspended == 1 for user in users)


def test_update_user_with_some_params(api_client, test_user):
    username, role, user_id = test_user

    is_success = api_client.admin.update_user(user_id=user_id, new_password='new password', is_suspended=False)

    users = api_client.admin.get_users()

    assert is_success is True
    assert any(user.username == username and user.role == role and user.suspended == 0 for user in users)


def test_update_user_raise_exception_with_username_with_spaces(api_client, test_user):
    _, _, user_id = test_user

    with pytest.raises(ApythingRequestException) as ex:
        api_client.admin.update_user(user_id=user_id, new_username="updated username", new_password='new password', new_role='admin', is_suspended=True)

    exception_msg = "Error: Username must only contain lowercase letters, numbers, underscores, and hyphens with no spaces"
    assert exception_msg in str(ex.value)    
