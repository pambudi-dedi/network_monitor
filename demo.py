#!/usr/bin/env python3
"""
Demo script untuk Network Monitor
Menunjukkan cara menggunakan aplikasi monitoring
"""
import sys
import time
import threading
import requests
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.monitor.network_monitor import NetworkMonitor
from src.database.db_manager import DatabaseManager

def simulate_network_activity():
    """Simulasi aktivitas jaringan untuk demo"""
    print("🚀 Starting network activity simulation...")
    
    # Simulasi beberapa request HTTP
    urls = [
        "https://www.google.com",
        "https://www.github.com", 
        "https://www.stackoverflow.com",
        "https://www.python.org",
        "https://www.docker.com"
    ]
    
    for i in range(10):
        try:
            url = urls[i % len(urls)]
            print(f"📡 Making request to {url}")
            response = requests.get(url, timeout=5)
            print(f"✅ Response: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)
    
    print("✅ Network simulation completed!")

def show_live_stats(db_manager):
    """Tampilkan statistik live"""
    print("\n📊 Live Statistics:")
    print("-" * 40)
    
    for i in range(5):
        stats = db_manager.get_connection_stats(1)  # Last 1 hour
        print(f"⏰ Update {i+1}:")
        print(f"   Total Connections: {stats.get('total_connections', 0)}")
        print(f"   Unique Domains: {stats.get('unique_domains', 0)}")
        print(f"   Data Transferred: {stats.get('total_data_mb', 0)} MB")
        print(f"   Suspicious: {stats.get('suspicious_connections', 0)}")
        
        # Show recent connections
        connections = db_manager.get_recent_connections(3)
        if connections:
            print("   Recent Connections:")
            for conn in connections:
                dest = conn['dest_domain'] or conn['dest_ip']
                status = "🚨" if conn['is_suspicious'] else "✅"
                print(f"     {status} {conn['source_ip']} -> {dest}:{conn['dest_port']}")
        
        print()
        time.sleep(3)
    
    print("📊 Statistics monitoring completed!")

def main():
    print("="*60)
    print("🌐 NETWORK MONITOR DEMO")
    print("="*60)
    print()
    
    # Initialize components
    print("🔧 Initializing components...")
    network_monitor = NetworkMonitor()
    db_manager = DatabaseManager()
    
    # Show network info
    print("📡 Network Information:")
    network_info = network_monitor.get_network_info()
    print(f"   Available Interfaces: {', '.join(network_info.get('available_interfaces', []))}")
    print(f"   Current Interface: {network_info.get('current_interface', 'Unknown')}")
    print()
    
    # Start monitoring
    print("🚀 Starting network monitoring...")
    network_monitor.start_monitoring()
    
    # Wait a bit for monitoring to start
    time.sleep(2)
    
    # Start network simulation in background
    simulation_thread = threading.Thread(target=simulate_network_activity)
    simulation_thread.daemon = True
    simulation_thread.start()
    
    # Show live stats
    show_live_stats(db_manager)
    
    # Show final statistics
    print("📈 Final Statistics:")
    print("-" * 40)
    final_stats = db_manager.get_connection_stats(24)
    print(f"Total Connections (24h): {final_stats.get('total_connections', 0)}")
    print(f"Unique Domains (24h): {final_stats.get('unique_domains', 0)}")
    print(f"Data Transferred (24h): {final_stats.get('total_data_mb', 0)} MB")
    print(f"Suspicious Connections (24h): {final_stats.get('suspicious_connections', 0)}")
    
    # Show top domains
    print("\n🏆 Top Domains:")
    top_domains = db_manager.get_top_domains(5)
    for i, domain in enumerate(top_domains, 1):
        print(f"   {i}. {domain['dest_domain']} - {domain['access_count']} accesses")
    
    # Show recent alerts
    print("\n🚨 Recent Alerts:")
    alerts = db_manager.get_recent_alerts(5)
    if alerts:
        for alert in alerts:
            severity_icon = "🔴" if alert['severity'] == 'CRITICAL' else "🟡" if alert['severity'] == 'WARNING' else "🔵"
            print(f"   {severity_icon} [{alert['severity']}] {alert['alert_type']}: {alert['message']}")
    else:
        print("   No alerts found")
    
    # Stop monitoring
    print("\n🛑 Stopping network monitoring...")
    network_monitor.stop_monitoring()
    
    print("\n" + "="*60)
    print("✅ Demo completed successfully!")
    print("="*60)
    print()
    print("💡 Tips:")
    print("   - Run 'python main.py --dashboard' to start web dashboard")
    print("   - Run 'python main.py --stats' to view statistics")
    print("   - Check logs/ directory for detailed logs")
    print("   - Web dashboard available at http://localhost:5000")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        sys.exit(1)
