import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_analytics_usage_and_performance_metrics():
    usage_url = f"{BASE_URL}/analytics/usage"
    performance_url = f"{BASE_URL}/analytics/performance"

    headers = {
        "Accept": "application/json"
    }

    try:
        # Test /analytics/usage endpoint with no filters
        usage_response = requests.get(usage_url, headers=headers, timeout=TIMEOUT)
        assert usage_response.status_code == 200, f"Expected status 200, got {usage_response.status_code}"
        usage_data = usage_response.json()
        # Validate expected keys in usage analytics response
        assert "total_queries" in usage_data and isinstance(usage_data["total_queries"], int), "'total_queries' missing or not integer"
        assert "unique_users" in usage_data and isinstance(usage_data["unique_users"], int), "'unique_users' missing or not integer"
        assert "avg_response_time" in usage_data and (isinstance(usage_data["avg_response_time"], float) or isinstance(usage_data["avg_response_time"], int)), "'avg_response_time' missing or not number"
        assert "popular_intents" in usage_data and isinstance(usage_data["popular_intents"], list), "'popular_intents' missing or not list"
        assert "top_queries" in usage_data and isinstance(usage_data["top_queries"], list), "'top_queries' missing or not list"

        # Optionally test /analytics/usage with query params (e.g., period)
        params = {"period": "last_7_days"}
        usage_response_filtered = requests.get(usage_url, headers=headers, params=params, timeout=TIMEOUT)
        assert usage_response_filtered.status_code == 200, f"Expected status 200, got {usage_response_filtered.status_code}"
        usage_filtered_data = usage_response_filtered.json()
        assert "total_queries" in usage_filtered_data, "Filtered 'total_queries' missing"
        
        # Test /analytics/performance endpoint
        performance_response = requests.get(performance_url, headers=headers, timeout=TIMEOUT)
        assert performance_response.status_code == 200, f"Expected status 200, got {performance_response.status_code}"
        performance_data = performance_response.json()
        # We expect a dict with some performance metrics info (no exact schema given)
        assert isinstance(performance_data, dict), "Performance data is not a dictionary"
        # Basic keys check if possible (since schema not detailed)
        # Check at least non-empty dict
        assert len(performance_data) > 0, "Performance metrics response is empty"

    except requests.RequestException as e:
        assert False, f"Request failed: {str(e)}"

    except ValueError as e:
        assert False, f"Response decoding failed: {str(e)}"

test_analytics_usage_and_performance_metrics()