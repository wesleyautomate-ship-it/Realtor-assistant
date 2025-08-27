import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_market_data_analytics_endpoints():
    headers = {
        "Accept": "application/json",
    }

    # Test /market/overview endpoint
    overview_url = f"{BASE_URL}/market/overview"
    try:
        overview_resp = requests.get(overview_url, headers=headers, timeout=TIMEOUT)
        assert overview_resp.status_code == 200, f"/market/overview status code {overview_resp.status_code}"
        overview_data = overview_resp.json()
        # Validate expected keys in overview response
        expected_keys = {
            "total_properties",
            "average_price",
            "price_trend",
            "rental_yield",
            "top_areas",
            "market_sentiment",
        }
        assert expected_keys.issubset(overview_data.keys()), "/market/overview missing expected keys"
        assert isinstance(overview_data["total_properties"], int)
        assert isinstance(overview_data["average_price"], (int, float))
        assert isinstance(overview_data["price_trend"], (int, float))
        assert isinstance(overview_data["rental_yield"], (int, float))
        assert isinstance(overview_data["top_areas"], list)
        assert isinstance(overview_data["market_sentiment"], str)
    except Exception as e:
        raise AssertionError(f"Failed testing /market/overview: {e}")

    # Test /market/areas/{area_name} endpoint
    # Use first top area if available; fallback to "Downtown" as default test area
    area_name = "Downtown"
    if "top_areas" in overview_data and overview_data["top_areas"]:
        first_area = overview_data["top_areas"][0]
        if isinstance(first_area, str) and first_area.strip():
            area_name = first_area.strip()

    area_url = f"{BASE_URL}/market/areas/{area_name}"
    try:
        area_resp = requests.get(area_url, headers=headers, timeout=TIMEOUT)
        assert area_resp.status_code == 200, f"/market/areas/{area_name} status code {area_resp.status_code}"
        area_data = area_resp.json()
        # At minimum, expect non-empty dict/JSON object for area data
        assert isinstance(area_data, dict), f"Expected dict response for area data, got {type(area_data)}"
        assert len(area_data) > 0, "/market/areas/{area_name} returned empty data"
    except Exception as e:
        raise AssertionError(f"Failed testing /market/areas/{area_name}: {e}")

    # Test /market/trends endpoint
    trends_url = f"{BASE_URL}/market/trends"
    # Test with parameters: area=area_name, property_type=example string, period=example string
    params = {
        "area": area_name,
        "property_type": "residential",
        "period": "1y"
    }
    try:
        trends_resp = requests.get(trends_url, headers=headers, params=params, timeout=TIMEOUT)
        assert trends_resp.status_code == 200, f"/market/trends status code {trends_resp.status_code}"
        trends_data = trends_resp.json()
        # Expect a JSON object with data, structure unspecified but must not be empty
        assert isinstance(trends_data, dict), f"Expected dict response for market trends, got {type(trends_data)}"
        assert len(trends_data) > 0, "/market/trends returned empty data"
    except Exception as e:
        raise AssertionError(f"Failed testing /market/trends: {e}")

test_market_data_analytics_endpoints()