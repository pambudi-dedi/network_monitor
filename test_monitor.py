#!/usr/bin/env python3
"""
Test script untuk Network Monitor
"""
import sys
import time
import requests
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.database.db_manager import DatabaseManager
from src.utils.geo_utils import GeoLocationUtils

def test_database():
    """Test database functionality"""
    print("Testing Database Manager...")
    
    db = DatabaseManager()
    
    # Test insert connection
    test_connection = {
        'source_ip': '192.168.1.100',
        'dest_ip': '8.8.8.8',
        'dest_port': 53,
        'protocol': 'UDP',
        'dest_domain': 'dns.google',
        'packet_size': 64,
        'connection_type': 'OUTBOUND',
        'country': 'United States',
        'is_suspicious': False,
        'raw_data': {'test': True}
    }
    
    result = db.insert_connection(test_connection)
    print(f"Insert connection: {'✓' if result else '✗'}")
    
    # Test get recent connections
    connections = db.get_recent_connections(5)
    print(f"Get recent connections: {'✓' if connections else '✗'} ({len(connections)} records)")
    
    # Test get stats
    stats = db.get_connection_stats(24)
    print(f"Get connection stats: {'✓' if stats else '✗'}")
    print(f"  - Total connections: {stats.get('total_connections', 0)}")
    print(f"  - Unique domains: {stats.get('unique_domains', 0)}")
    
    # Test insert alert
    alert_result = db.insert_alert('TEST', 'Test alert message', 'INFO')
    print(f"Insert alert: {'✓' if alert_result else '✗'}")
    
    print("Database test completed!\n")

def test_geo_utils():
    """Test geolocation utilities"""
    print("Testing GeoLocation Utils...")
    
    geo = GeoLocationUtils()
    
    # Test public IP
    test_ips = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
    
    for ip in test_ips:
        country = geo.get_country(ip)
        print(f"IP {ip}: {country}")
    
    # Test private IP
    private_ip = '192.168.1.1'
    country = geo.get_country(private_ip)
    print(f"Private IP {private_ip}: {country}")
    
    # Test my public IP
    my_ip = geo.get_my_ip()
    print(f"My public IP: {my_ip}")
    
    print("GeoLocation test completed!\n")

def test_web_api():
    """Test web API endpoints"""
    print("Testing Web API...")
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        '/api/stats',
        '/api/connections',
        '/api/domains',
        '/api/alerts',
        '/api/network-info'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"GET {endpoint}: {status} ({response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"GET {endpoint}: ✗ (Connection failed)")
    
    print("Web API test completed!\n")

def main():
    print("="*50)
    print("NETWORK MONITOR TEST SUITE")
    print("="*50)
    
    # Test database
    test_database()
    
    # Test geolocation
    test_geo_utils()
    
    # Test web API (if dashboard is running)
    print("Testing Web API (make sure dashboard is running)...")
    test_web_api()
    
    print("="*50)
    print("All tests completed!")
    print("="*50)

if __name__ == '__main__':
    main()
