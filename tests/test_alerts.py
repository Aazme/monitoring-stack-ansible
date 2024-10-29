import json
import pytest
import time

PROMETHEUS_URL = "http://localhost:9090"
LOKI_URL = "http://localhost:3100"

# Fixture for querying Prometheus alerts from the target host
@pytest.fixture
def query_prometheus_alerts(host):
    def _query():
        cmd = host.run(f"curl -s {PROMETHEUS_URL}/api/v1/alerts")
        assert cmd.rc == 0, f"Failed to query Prometheus alerts: {cmd.stderr}"
        return json.loads(cmd.stdout)
    return _query

# Function to wait for a specific alert to fire
def wait_for_alert_to_fire(host, query_func, alert_name, timeout=180, interval=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        response = query_func()
        alerts = [
            alert for alert in response['data']['alerts']
            if alert['labels'].get('alertname') == alert_name and alert['state'] == 'firing'
        ]
        if alerts:
            return True
        time.sleep(interval)
    return False

def test_high_memory_alert(host, query_prometheus_alerts):
    stress_command = (
        "stress --vm-bytes $(awk '/MemAvailable/ {printf \"%d\\n\", $2 * 0.85;}' /proc/meminfo)k --vm-keep -m 1 &"
    )
    try:
        host.run(stress_command)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighMemoryUsage')
        assert alert_fired, "HighMemoryUsage alert did not fire as expected"
    finally:
        host.run("pkill -f 'stress'")

def test_high_cpu_alert(host, query_prometheus_alerts):
    cpu_stress_command = "stress --cpu $(nproc) --timeout 90 &"
    try:
        host.run(cpu_stress_command)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighCPUUsage')
        assert alert_fired, "HighCPUUsage alert did not fire as expected"
    finally:
        host.run("pkill -f 'stress'")

def test_disk_space_low_alert(host, query_prometheus_alerts):
    big_file_command = "fallocate -l $(df --output=avail / | tail -1 | awk '{print int($1*0.9)}')K /tmp/bigfile"
    try:
        host.run(big_file_command)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'DiskSpaceLow')
        assert alert_fired, "DiskSpaceLow alert did not fire as expected"
    finally:
        host.run("rm -f /tmp/bigfile")

def test_high_disk_io_alert(host, query_prometheus_alerts):
    disk_io_command = "dd if=/dev/zero of=/tmp/testfile bs=3M count=4000"
    try:
        host.run(disk_io_command)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighDiskIOUsage')
        assert alert_fired, "HighDiskIOUsage alert did not fire as expected"
    finally:
        host.run("rm -f /tmp/testfile")

def test_node_exporter_down_alert(host, query_prometheus_alerts):
    try:
        host.run("docker stop node-exporter")
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'NodeExporterDown', timeout=300)
        assert alert_fired, "NodeExporterDown alert did not fire as expected"
    finally:
        host.run("docker start node-exporter")

def test_grafana_down_alert(host, query_prometheus_alerts):
    try:
        host.run("docker stop grafana")
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'GrafanaDown', timeout=300)
        assert alert_fired, "NodeExporterDown alert did not fire as expected"
    finally:
        host.run("docker start grafana")
