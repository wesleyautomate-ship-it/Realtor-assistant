import requests

base_url = "http://localhost:8000"
timeout = 30

def test_authentication_api_key_generation():
    # Step 1: Register a new user
    register_url = f"{base_url}/auth/register"
    register_payload = {
        "username": "testuser_api_key_gen",
        "email": "testuser_api_key_gen@example.com",
        "password": "StrongPassw0rd!"
    }
    try:
        response = requests.post(register_url, json=register_payload, timeout=timeout)
        assert response.status_code == 201, f"User registration failed: {response.text}"

        # Step 2: Login the user to get access token
        login_url = f"{base_url}/auth/login"
        login_payload = {
            "username": register_payload["username"],
            "password": register_payload["password"]
        }
        response = requests.post(login_url, json=login_payload, timeout=timeout)
        assert response.status_code == 200, f"User login failed: {response.text}"
        login_data = response.json()
        assert "access_token" in login_data, "Access token missing in login response"
        access_token = login_data["access_token"]

        # Step 3: Generate API key using the access token (authenticated)
        gen_key_url = f"{base_url}/auth/generate-key"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(gen_key_url, headers=headers, timeout=timeout)
        assert response.status_code == 200, f"API key generation failed: {response.text}"
        data = response.json()
        assert "api_key" in data, "API key missing in generation response"
        api_key = data["api_key"]
        assert isinstance(api_key, str) and len(api_key) > 0, "Invalid API key format"

        # Step 4: Test unauthorized access to generate-key endpoint
        response = requests.post(gen_key_url, timeout=timeout)
        assert response.status_code in (401, 403), "Unauthorized API key generation request did not fail as expected"

    finally:
        # Cleanup: if platform supports user deletion via API, implement here (not specified in PRD)
        # No deletion endpoint provided for users; so no cleanup step for user removal.
        pass

test_authentication_api_key_generation()