import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_property_management_crud_and_filtering():
    # Sample property data for creation
    property_data = {
        "title": f"Test Property {uuid.uuid4()}",
        "description": "A beautiful apartment in Dubai Marina.",
        "location": "Dubai Marina",
        "property_type": "Apartment",
        "price": 1500000.00,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1200.5
    }
    property_id = None

    try:
        # CREATE property
        create_resp = requests.post(
            f"{BASE_URL}/properties",
            json=property_data,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert create_resp.status_code == 200, f"Property creation failed: {create_resp.text}"
        resp_json = create_resp.json()
        property_id = resp_json.get("id") or resp_json.get("property_id")
        assert property_id is not None, "Property ID not found in creation response"
        property_id = int(property_id)

        # RETRIEVE property by ID
        get_resp = requests.get(f"{BASE_URL}/properties/{property_id}", timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Get property failed: {get_resp.text}"
        prop_detail = get_resp.json()
        # Validate fields
        for key in property_data:
            assert key in prop_detail, f"Field {key} missing in property detail"
        assert prop_detail["title"] == property_data["title"], "Title mismatch"
        assert prop_detail["location"] == property_data["location"], "Location mismatch"

        # UPDATE property
        update_data = {
            "title": property_data["title"] + " Updated",
            "description": "Updated description with sea view.",
            "location": property_data["location"],
            "property_type": property_data["property_type"],
            "price": property_data["price"] + 200000,
            "bedrooms": property_data["bedrooms"],
            "bathrooms": property_data["bathrooms"],
            "area": property_data["area"]
        }
        update_resp = requests.put(
            f"{BASE_URL}/properties/{property_id}",
            json=update_data,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert update_resp.status_code == 200, f"Update failed: {update_resp.text}"

        # VERIFY update
        get_updated_resp = requests.get(f"{BASE_URL}/properties/{property_id}", timeout=TIMEOUT)
        assert get_updated_resp.status_code == 200, f"Get updated property failed: {get_updated_resp.text}"
        updated_detail = get_updated_resp.json()
        assert updated_detail["title"] == update_data["title"], "Updated title mismatch"
        assert updated_detail["price"] == update_data["price"], "Updated price mismatch"

        # FILTER properties with pagination
        params = {
            "page": 1,
            "limit": 5,
            "location": "Dubai Marina",
            "min_price": 1000000,
            "max_price": 2000000,
            "property_type": "Apartment"
        }
        filter_resp = requests.get(f"{BASE_URL}/properties", params=params, timeout=TIMEOUT)
        assert filter_resp.status_code == 200, f"Filter request failed: {filter_resp.text}"
        filter_result = filter_resp.json()
        assert "properties" in filter_result and isinstance(filter_result["properties"], list), "Properties list missing"
        assert "total" in filter_result and isinstance(filter_result["total"], int), "Total count missing"
        assert "page" in filter_result and filter_result["page"] == 1, "Page number mismatch"
        assert "limit" in filter_result and filter_result["limit"] == 5, "Limit mismatch"
        # Check if the updated_property is in filtered results
        ids_in_results = [p.get("id") or p.get("property_id") for p in filter_result["properties"]]
        assert property_id in ids_in_results, "Updated property not found in filter results"

    finally:
        # CLEANUP: delete the created property if exists
        if property_id is not None:
            del_resp = requests.delete(f"{BASE_URL}/properties/{property_id}", timeout=TIMEOUT)
            assert del_resp.status_code == 204, f"Delete property failed: {del_resp.text}"

test_property_management_crud_and_filtering()
