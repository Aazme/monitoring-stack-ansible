import pytest



def test_docker_is_installed(host):
    docker = host.package("docker-ce")
    assert docker.is_installed

def test_services_are_running_and_enabled(host):
    services = ["docker"]
    for service_name in services:
        service = host.service(service_name)
        assert service.is_running
        assert service.is_enabled

def test_docker_containers_are_running(host):
    containers = [
        "prometheus",
        "grafana",
        "loki",
        "alertmanager",
        "node-exporter",
        "cadvisor",
    ]
    for container_name in containers:
        container = host.docker(container_name)
        assert container.is_running

def test_ports_are_listening(host):
    ports = [
        ("0.0.0.0", 9090),   # Prometheus
        ("0.0.0.0", 3000),   # Grafana
        ("0.0.0.0", 9093),   # AlertManager
        ("0.0.0.0", 9100),   # Node Exporter
        ("0.0.0.0", 8080),   # cAdvisor
        ("0.0.0.0", 3100),   # Loki
    ]
    for address, port in ports:
        socket = host.socket("tcp://{}:{}".format(address, port))
        assert socket.is_listening

def test_prometheus_targets_are_up(host):
    cmd = host.run("curl -s http://localhost:9090/api/v1/targets")
    assert cmd.rc == 0
    import json
    targets = json.loads(cmd.stdout)
    for target in targets['data']['activeTargets']:
        assert target['health'] == 'up'