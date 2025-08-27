import requests
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_health_check_and_system_status_endpoints():
    headers = {
        "Accept": "application/json"
    }
    # Test /health endpoint
    try:
        response_health = requests.get(f"{BASE_URL}/health", headers=headers, timeout=TIMEOUT)
        response_health.raise_for_status()
    except (HTTPError, Timeout, ConnectionError, RequestException) as e:
        assert False, f"/health endpoint request failed: {str(e)}"
    data_health = response_health.json()
    assert "status" in data_health, "Missing 'status' in /health response"
    assert isinstance(data_health["status"], str), "'status' should be a string in /health response"
    assert data_health["status"].lower() == "healthy" or data_health["status"].lower() == "ok" or data_health["status"].lower() == "up", \
        f"Unexpected health status value: {data_health['status']}"
    assert "timestamp" in data_health, "Missing 'timestamp' in /health response"
    assert "version" in data_health, "Missing 'version' in /health response"
    assert "services" in data_health, "Missing 'services' in /health response"
    assert isinstance(data_health["services"], dict), "'services' should be an object in /health response"

    # Test /status endpoint
    try:
        response_status = requests.get(f"{BASE_URL}/status", headers=headers, timeout=TIMEOUT)
        response_status.raise_for_status()
    except (HTTPError, Timeout, ConnectionError, RequestException) as e:
        assert False, f"/status endpoint request failed: {str(e)}"
    data_status = response_status.json()
    # Validate required fields in /status response
    required_fields = {
        "uptime": str,
        "memory_usage": str,
        "cpu_usage": str,
        "active_connections": int,
        "total_queries": int,
    }
    for field, typ in required_fields.items():
        assert field in data_status, f"Missing '{field}' in /status response"
        assert isinstance(data_status[field], typ), f"'{field}' should be of type {typ.__name__} in /status response"

test_health_check_and_system_status_endpoints()