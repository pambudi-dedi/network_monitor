"""
Konfigurasi untuk Network Monitor
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = BASE_DIR / "logs" / "network_monitor.db"

# Monitoring configuration
MONITORING_CONFIG = {
    "interface": "eth0",  # Default network interface
    "capture_timeout": 1,  # Timeout in seconds
    "max_packets": 1000,  # Maximum packets to capture
    "log_interval": 60,   # Log interval in seconds
}

# Web dashboard configuration
DASHBOARD_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
}

# Logging configuration
LOGGING_CONFIG = {
    "log_file": BASE_DIR / "logs" / "monitor.log",
    "log_level": "INFO",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

# Filtered domains (untuk mengabaikan traffic internal)
FILTERED_DOMAINS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
]

# Alert thresholds
ALERT_THRESHOLDS = {
    "max_connections_per_minute": 100,
    "suspicious_domains": [
        "malware.com",
        "phishing.com",
        "suspicious.com"
    ]
}
