# tests/test_loki_integration.py
import json
import time
import testinfra
from pytest import fail

def test_alpine_log_delivery_to_loki(host, setup_alpine_container):
    """Test that logs from a test Alpine container are delivered to Loki."""
    # Extract container details from the fixture
    container_name, log_message = setup_alpine_container

    loki_host = "localhost"  # Adjust if Loki is on a different host
    loki_port = "3100"
    loki_url = f"http://{loki_host}:{loki_port}/loki/api/v1/query"
    sleep_duration = 10  # Adjust based on expected log ingestion time

    try:
        print(f"Container {container_name} started successfully. Waiting for logs to be ingested by Loki.")
        time.sleep(sleep_duration)

        # Query Loki for the logs
        query = f'{{container_name="{container_name}"}}'
        print(f"Querying Loki at {loki_url} with query: {query}")
        result = host.run(f"curl -G '{loki_url}' --data-urlencode 'query={query}'")

        # Ensure the curl command executed successfully
        if result.rc != 0:
            fail(f"Failed to query Loki: {result.stderr}")

        # Parse the response and verify the log message
        response_json = json.loads(result.stdout)
        logs = response_json.get("data", {}).get("result", [])

        # Verify the presence of the log message in the logs
        if not any(log_message in entry.get("values", [[]])[0][1] for entry in logs):
            fail("Log message not found in Loki response")

        print("Test passed: Log message was successfully delivered to Loki.")

    except Exception as e:
        # Handle unexpected exceptions
        fail(f"An unexpected error occurred: {str(e)}")
