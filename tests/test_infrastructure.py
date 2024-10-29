# tests/test_infrastructure.py
import testinfra

def test_docker_is_installed(host):
    """Ensure Docker is installed."""
    docker = host.package("docker-ce")
    assert docker.is_installed
