import requests
import uuid
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_chat_api_with_rag_context():
    # Step 1: Register a new user
    register_url = f"{BASE_URL}/auth/register"
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    register_payload = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "TestPassword123!"
    }
    register_resp = requests.post(register_url, json=register_payload, timeout=TIMEOUT)
    assert register_resp.status_code == 201, f"User registration failed: {register_resp.text}"

    # Step 2: Login to get access token
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {
        "username": unique_username,
        "password": "TestPassword123!"
    }
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"User login failed: {login_resp.text}"
    login_data = login_resp.json()
    assert "access_token" in login_data and "token_type" in login_data
    token = login_data["access_token"]
    token_type = login_data["token_type"]
    headers_auth = {"Authorization": f"{token_type} {token}"}

    # Step 3: Upload a sample document to ingestion system to provide RAG context
    ingest_upload_url = f"{BASE_URL}/ingest/upload"
    file_content = b"Sample document text about Dubai real estate market."
    files = {
        "file": ("sample_doc.txt", file_content, "text/plain")
    }
    data = {
        "category": "market_report",
        "metadata": '{"source":"test"}'
    }
    ingest_resp = requests.post(ingest_upload_url, headers=headers_auth, files=files, data=data, timeout=TIMEOUT)
    assert ingest_resp.status_code == 200, f"Document ingestion upload failed: {ingest_resp.text}"
    ingest_data = ingest_resp.json()
    file_id = ingest_data.get("file_id")
    assert file_id, "file_id not returned by ingestion upload"

    # Step 4: Wait for document ingestion processing to complete (poll status)
    ingest_status_url = f"{BASE_URL}/ingest/status/{file_id}"
    max_wait = 60  # max 60 sec wait
    poll_interval = 5
    elapsed = 0
    while elapsed < max_wait:
        status_resp = requests.get(ingest_status_url, headers=headers_auth, timeout=TIMEOUT)
        assert status_resp.status_code == 200, f"Ingestion status check failed: {status_resp.text}"
        status_data = status_resp.json()
        if status_data.get("status") == "processed":
            break
        time.sleep(poll_interval)
        elapsed += poll_interval
    else:
        assert False, "Document ingestion did not complete in expected time"

    # Step 5: Use the /chat endpoint to send a message with RAG context (using context from ingested doc)
    chat_url = f"{BASE_URL}/chat"
    chat_payload = {
        "message": "What is the current market trend for Dubai properties?",
        "user_id": unique_username,
        "session_id": str(uuid.uuid4()),
        "context": {
            "related_documents": [file_id],
            "category": "market_report"
        }
    }
    chat_resp = requests.post(chat_url, headers=headers_auth, json=chat_payload, timeout=TIMEOUT)
    assert chat_resp.status_code == 200, f"Chat API call failed: {chat_resp.text}"
    chat_data = chat_resp.json()

    # Validate response fields
    assert "response" in chat_data and isinstance(chat_data["response"], str) and chat_data["response"], "Missing or invalid 'response'"
    assert "intent" in chat_data and isinstance(chat_data["intent"], str) and chat_data["intent"], "Missing or invalid 'intent'"
    assert "confidence" in chat_data and isinstance(chat_data["confidence"], (float, int)), "Missing or invalid 'confidence'"
    assert 0.0 <= chat_data["confidence"] <= 1.0, "'confidence' should be between 0 and 1"
    assert "context_used" in chat_data and isinstance(chat_data["context_used"], list), "Missing or invalid 'context_used'"
    assert "suggestions" in chat_data and isinstance(chat_data["suggestions"], list), "Missing or invalid 'suggestions'"

    # Optional additional checks: response not empty, intent meaningful, confidence above threshold, context_used non-empty
    assert chat_data["response"].strip() != "", "'response' is empty"
    assert chat_data["intent"].strip() != "", "'intent' is empty"
    assert chat_data["confidence"] > 0.5, "Confidence score is too low"
    # context_used should contain at least one entry related to file_id or relevant context
    assert any(isinstance(item, str) or isinstance(item, dict) for item in chat_data["context_used"]), "'context_used' does not contain valid items"


test_chat_api_with_rag_context()