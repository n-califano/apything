def test_get_users(api_client):
    # Setup
    #TODO: create a user

    users = api_client.admin.get_users()
    
    assert len(users) != 0
    #TODO: add asserts on ad hoc created user

    # Teardown
    #TODO: remove user

    

    
