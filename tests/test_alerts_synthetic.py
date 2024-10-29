import json
import pytest
import time

PROMETHEUS_URL = "http://localhost:9090"
PUSHGATEWAY_URL = "http://localhost:9091"

# Function to push custom metrics to Prometheus Pushgateway
def push_metric(host, job, instance, metric_name, value):
    url = f"{PUSHGATEWAY_URL}/metrics/job/{job}/instance/{instance}"
    data = f"{metric_name} {value}\n"
    cmd = host.run(f"curl -X POST --data '{data}' {url}")
    assert cmd.rc == 0, f"Failed to push metric {metric_name}: {cmd.stderr}"

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

# Test High Memory Usage Alert
def test_high_memory_alert(host, query_prometheus_alerts):
    try:
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemTotal_bytes", value=2000000000)
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=10)
        time.sleep(2)
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=10)
        time.sleep(2)
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=10)
        time.sleep(2)
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=10)
        time.sleep(2)
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=10)
        time.sleep(2)

        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighMemoryUsage')
        assert alert_fired, "HighMemoryUsage alert did not fire as expected"
    finally:
        push_metric(host, job="memory_test", instance="localhost", metric_name="node_memory_MemAvailable_bytes", value=1500000000)

# Test High CPU Usage Alert
def test_high_cpu_alert(host, query_prometheus_alerts):
    try:
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total", value=10000)
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=10)
        time.sleep(2)
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=10)
        time.sleep(2)
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=10)
        time.sleep(2)
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=10)
        time.sleep(2)
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=10)
        time.sleep(2)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighCPUUsage')
        assert alert_fired, "HighCPUUsage alert did not fire as expected"
    finally:
        push_metric(host, job="cpu_test", instance="localhost", metric_name="node_cpu_seconds_total{mode=\"idle\"}", value=80)

# Test Disk Space Low Alert
def test_disk_space_low_alert(host, query_prometheus_alerts):
    try:
        push_metric(host, job="disk_test", instance="localhost", metric_name="node_filesystem_size_bytes", value=10000000000)
        push_metric(host, job="disk_test", instance="localhost", metric_name="node_filesystem_avail_bytes", value=1000)
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'DiskSpaceLow')
        assert alert_fired, "DiskSpaceLow alert did not fire as expected"
    finally:
        push_metric(host, job="disk_test", instance="localhost", metric_name="node_filesystem_avail_bytes", value=5000000000)

# Test High Disk I/O Usage Alert
def test_high_disk_io_alert(host, query_prometheus_alerts):
    try:
        # Push metrics with different values to simulate increasing disk I/O usage
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=2000)
        time.sleep(2)  # Delay to allow Prometheus to register
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=3000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=4000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=5000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=6000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=7000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=8000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=9000)
        time.sleep(2)
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=10000)
        
        # Wait for the alert to fire
        alert_fired = wait_for_alert_to_fire(host, query_prometheus_alerts, 'HighDiskIOUsage')
        assert alert_fired, "HighDiskIOUsage alert did not fire as expected"
    finally:
        # Reset the metric value to avoid persistent alert
        push_metric(host, job="disk_io_test", instance="localhost", metric_name="node_disk_io_time_seconds_total", value=30)