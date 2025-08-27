import requests
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_document_ingestion_upload_and_status():
    # This test requires a file to upload, use a small sample text file content
    file_content = b"Sample document content for testing document ingestion upload."
    files = {
        'file': ('test_document.txt', file_content, 'text/plain')
    }
    data = {
        'category': 'test-category',
        'metadata': '{"source":"unittest"}'
    }
    headers = {}

    file_id = None

    try:
        # Step 1: Upload the document via /ingest/upload endpoint
        upload_response = requests.post(
            f"{BASE_URL}/ingest/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=TIMEOUT
        )
        assert upload_response.status_code == 200, f"Upload failed: {upload_response.text}"
        upload_json = upload_response.json()
        assert 'file_id' in upload_json, "Response missing file_id"
        assert upload_json.get('filename') == 'test_document.txt'
        assert upload_json.get('category') == 'test-category'
        assert 'status' in upload_json and isinstance(upload_json['status'], str)
        assert 'pages' in upload_json and isinstance(upload_json['pages'], int)
        assert 'extracted_text' in upload_json and isinstance(upload_json['extracted_text'], str)
        file_id = upload_json['file_id']

        # Step 2: Poll /ingest/status/{file_id} until processing is done or timeout after ~30s
        status_url = f"{BASE_URL}/ingest/status/{file_id}"
        max_attempts = 6
        delay = 5  # seconds
        status_response = None
        for _ in range(max_attempts):
            status_response = requests.get(status_url, timeout=TIMEOUT)
            assert status_response.status_code == 200, f"Status check failed: {status_response.text}"
            status_json = status_response.json()
            assert 'status' in status_json and isinstance(status_json['status'], str)
            if status_json['status'].lower() in ('completed', 'processed', 'done', 'finished'):
                break
            time.sleep(delay)
        else:
            # After retries, if not finished, fail
            raise AssertionError("Document processing did not complete in expected time.")

        # Validate the final status response fields
        assert 'file_id' in status_json and status_json['file_id'] == file_id
        assert 'filename' in status_json and status_json['filename'] == 'test_document.txt'
        assert 'category' in status_json and status_json['category'] == 'test-category'
        assert 'pages' in status_json and isinstance(status_json['pages'], int)
        assert 'extracted_text' in status_json and isinstance(status_json['extracted_text'], str)

    finally:
        # Cleanup: If the API supports document deletion, delete after test
        # Not specified in PRD so skip actual deletion
        pass

test_document_ingestion_upload_and_status()