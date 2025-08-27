import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}


def test_client_management_crud_and_filtering():
    # Generate unique client data for creation
    unique_suffix = str(uuid.uuid4())
    client_data = {
        "name": f"Test Client {unique_suffix}",
        "email": f"testclient{unique_suffix}@example.com",
        "phone": "+971501234567",
        "preferences": {
            "property_type": "apartment",
            "budget": 1000000,
            "locations": ["Dubai Marina", "Jumeirah Beach Residence"]
        }
    }

    client_id = None
    try:
        # 1. Create a new client record via POST /clients
        create_resp = requests.post(
            f"{BASE_URL}/clients",
            headers=HEADERS,
            json=client_data,
            timeout=TIMEOUT,
        )
        assert create_resp.status_code == 201, f"Create client failed: {create_resp.text}"
        created_client = create_resp.json()
        assert isinstance(created_client, dict)

        # Extract client_id - assuming API returns id field on creation
        client_id = created_client.get("id") or created_client.get("client_id")
        assert client_id is not None, "Created client response missing 'id'"

        # 2. Retrieve clients with filtering and pagination using GET /clients
        # Test general listing first without filter
        list_resp = requests.get(
            f"{BASE_URL}/clients",
            headers=HEADERS,
            params={"page": 1, "limit": 10},
            timeout=TIMEOUT,
        )
        assert list_resp.status_code == 200, f"List clients failed: {list_resp.text}"
        list_data = list_resp.json()
        assert isinstance(list_data, dict)
        assert "clients" in list_data or isinstance(list_data.get("items"), list), "Client list response missing expected keys"

        # 3. Retrieve clients filtered by search term (client name)
        filter_resp = requests.get(
            f"{BASE_URL}/clients",
            headers=HEADERS,
            params={"search": client_data["name"][:10]},  # partial search
            timeout=TIMEOUT,
        )
        assert filter_resp.status_code == 200, f"Filtered clients retrieval failed: {filter_resp.text}"
        filtered_clients = filter_resp.json()
        assert isinstance(filtered_clients, dict)
        found_clients = filtered_clients.get("clients") or filtered_clients.get("items") or []
        assert any(client_data["name"] in (c.get("name") or "") for c in found_clients), "Created client not found in filtered search"

        # 4. Retrieve clients filtered by status (assuming status possible)
        # Use a generic status filter test
        status_resp = requests.get(
            f"{BASE_URL}/clients",
            headers=HEADERS,
            params={"status": "active", "limit": 5},
            timeout=TIMEOUT,
        )
        assert status_resp.status_code == 200, f"Status filtered clients retrieval failed: {status_resp.text}"
        status_clients = status_resp.json()
        assert isinstance(status_clients, dict)

        # 5. Verify that client preferences and contact information are handled properly
        # Get client detail by filtering to our client and checking preferences/contact
        # Since no GET by id is defined, we re-fetch filtered by search unique email or name exactly
        exact_search_resp = requests.get(
            f"{BASE_URL}/clients",
            headers=HEADERS,
            params={"search": client_data["email"]},
            timeout=TIMEOUT,
        )
        assert exact_search_resp.status_code == 200, f"Exact search client retrieval failed: {exact_search_resp.text}"
        exact_clients = exact_search_resp.json()
        candidates = exact_clients.get("clients") or exact_clients.get("items") or []
        client_record = None
        for cl in candidates:
            if cl.get("email") == client_data["email"]:
                client_record = cl
                break
        assert client_record is not None, "Created client record not found by email search"
        # Check that preferences and contact info match created data
        assert client_record.get("preferences") == client_data["preferences"], "Client preferences mismatch"
        assert client_record.get("phone") == client_data["phone"], "Client phone mismatch"
        assert client_record.get("name") == client_data["name"], "Client name mismatch"
        assert client_record.get("email") == client_data["email"], "Client email mismatch"

    finally:
        # If we created a client, try to delete it if DELETE endpoint exists (not specified in PRD)
        if client_id is not None:
            try:
                del_resp = requests.delete(
                    f"{BASE_URL}/clients/{client_id}",
                    headers=HEADERS,
                    timeout=TIMEOUT,
                )
                # If DELETE not supported, ignore 404 or 405 errors
                if del_resp.status_code not in (204, 404, 405):
                    raise AssertionError(f"Failed to delete test client {client_id}, status: {del_resp.status_code}, body: {del_resp.text}")
            except requests.RequestException:
                # If delete request fails, log but do not raise to not mask test results
                pass


test_client_management_crud_and_filtering()