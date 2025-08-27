import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_authentication_user_registration_and_login():
    register_url = f"{BASE_URL}/auth/register"
    login_url = f"{BASE_URL}/auth/login"

    # Generate unique username and email for test isolation
    unique_id = str(uuid.uuid4())
    username = f"testuser_{unique_id}"
    email = f"{username}@example.com"
    password = "StrongPass!123"

    registration_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    headers = {"Content-Type": "application/json"}

    # Register the user
    try:
        reg_response = requests.post(register_url, json=registration_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"User registration request failed: {e}"

    assert reg_response.status_code == 201, f"Expected status 201 for registration, got {reg_response.status_code}"
    reg_json = reg_response.json()
    assert isinstance(reg_json, dict), "Registration response is not a JSON object"

    # Login the registered user
    login_payload = {
        "username": username,
        "password": password
    }
    try:
        login_response = requests.post(login_url, json=login_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"User login request failed: {e}"

    assert login_response.status_code == 200, f"Expected status 200 for login, got {login_response.status_code}"
    login_json = login_response.json()
    assert "access_token" in login_json, "Login response missing access_token"
    assert isinstance(login_json["access_token"], str) and len(login_json["access_token"]) > 0, "Invalid access_token"
    assert "token_type" in login_json, "Login response missing token_type"
    assert login_json["token_type"].lower() == "bearer", "token_type is not 'bearer'"

    access_token = login_json["access_token"]

    # Negative test: Attempt login with wrong password
    wrong_login_payload = {
        "username": username,
        "password": "WrongPassword!456"
    }
    try:
        wrong_login_response = requests.post(login_url, json=wrong_login_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Failed request for wrong password login test: {e}"

    assert wrong_login_response.status_code in (401, 403), f"Expected 401 or 403 for wrong password login, got {wrong_login_response.status_code}"

    # Negative test: Attempt registration with same username/email (expect failure)
    try:
        dup_reg_response = requests.post(register_url, json=registration_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Duplicate registration request failed: {e}"

    # Depending on implementation, it may return 400 or 409 for duplicates
    assert dup_reg_response.status_code in (400, 409), f"Expected 400 or 409 for duplicate registration, got {dup_reg_response.status_code}"

test_authentication_user_registration_and_login()