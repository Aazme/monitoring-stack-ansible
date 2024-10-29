# tests/conftest.py
import pytest

@pytest.fixture
def setup_alpine_container(host):
    """Sets up a test Alpine container and yields its name and log message."""
    container_name = "test-log-container"
    log_message = "Test log message for Loki"

    # Run an alpine container on the target host and generate a log message
    host.run(f"docker run --name {container_name} alpine sh -c 'echo \"{log_message}\"; sleep 5'")

    yield container_name, log_message

    # Cleanup after the test is done
    host.run(f"docker rm -f {container_name}")
