import subprocess
import socket
import json
import time

def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "4", host],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return str(e)

def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        return str(e)

def analyze_ping_output(output):
    lines = output.splitlines()
    stats = {
        "packet_loss": None,
        "avg_latency_ms": None
    }

    for line in lines:
        if "Lost" in line:
            parts = line.split(",")
            for p in parts:
                if "Lost" in p:
                    stats["packet_loss"] = p.strip()
        if "Average" in line:
            avg = line.split("Average =")[-1].replace("ms", "").strip()
            stats["avg_latency_ms"] = avg

    return stats

def run_network_diagnostics():
    hosts = ["8.8.8.8", "1.1.1.1", "google.com", "cloudflare.com"]
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": []
    }

    for host in hosts:
        print(f"Testing: {host}")
        ping_output = ping_host(host)
        dns_result = dns_lookup(host) if not host.replace(".", "").isdigit() else "N/A"
        stats = analyze_ping_output(ping_output)

        report["results"].append({
            "host": host,
            "dns_lookup": dns_result,
            "ping_output": ping_output,
            "packet_loss": stats["packet_loss"],
            "avg_latency_ms": stats["avg_latency_ms"]
        })

    with open("network_report.json", "
