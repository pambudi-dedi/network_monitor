#!/usr/bin/env python3
"""
Network Monitor - Aplikasi utama untuk monitoring network traffic
"""
import sys
import os
import argparse
import logging
import signal
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from config.config import LOGGING_CONFIG, MONITORING_CONFIG
from src.monitor.network_monitor import NetworkMonitor
from src.monitor.process_monitor import ProcessMonitor
from src.database.db_manager import DatabaseManager
from src.dashboard.app import app

class NetworkMonitorApp:
    def __init__(self):
        self.network_monitor = None
        self.process_monitor = ProcessMonitor()
        self.db_manager = DatabaseManager()
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory
        log_file = Path(LOGGING_CONFIG['log_file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, LOGGING_CONFIG['log_level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def start_monitoring(self, interface: str = None):
        """Start network monitoring"""
        try:
            self.logger.info("Starting Network Monitor Application...")
            
            # Initialize network monitor
            self.network_monitor = NetworkMonitor(interface)
            
            # Start monitoring
            self.network_monitor.start_monitoring()
            
            self.logger.info("Network monitoring started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        try:
            if self.network_monitor:
                self.network_monitor.stop_monitoring()
                self.logger.info("Network monitoring stopped")
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
    
    def run_dashboard(self, host: str = "0.0.0.0", port: int = 5000):
        """Run web dashboard"""
        try:
            self.logger.info(f"Starting web dashboard on {host}:{port}")
            app.run(host=host, port=port, debug=False)
        except Exception as e:
            self.logger.error(f"Error running dashboard: {e}")
    
    def monitor_application(self, app_name: str, duration: int = 300):
        """Monitor aplikasi spesifik"""
        try:
            self.logger.info(f"Starting {app_name} monitoring for {duration} seconds...")
            
            print(f"\n🎯 Monitoring {app_name.upper()} Network Activity")
            print("=" * 50)
            
            # Check if application is running
            processes = self.process_monitor.get_process_by_name(app_name)
            if not processes:
                print(f"❌ {app_name} tidak ditemukan. Pastikan aplikasi sedang berjalan.")
                return
            
            print(f"✅ {app_name} ditemukan! ({len(processes)} processes)")
            for proc in processes:
                print(f"   PID {proc['pid']}: {proc['name']}")
            
            # Monitor for specified duration
            start_time = time.time()
            end_time = start_time + duration
            
            destinations = {}
            total_connections = 0
            
            while time.time() < end_time:
                # Get current connections
                if app_name.lower() == 'discord':
                    connections = self.process_monitor.get_discord_connections()
                else:
                    # Generic process monitoring
                    connections = []
                    for proc in processes:
                        proc_connections = self.process_monitor._get_process_connections(proc['pid'])
                        for conn in proc_connections:
                            if conn['remote_address'] and conn['remote_port']:
                                connections.append({
                                    'process_name': proc['name'],
                                    'pid': proc['pid'],
                                    'remote_address': conn['remote_address'],
                                    'remote_port': conn['remote_port'],
                                    'local_address': conn['local_address'],
                                    'local_port': conn['local_port']
                                })
                
                total_connections = len(connections)
                
                # Update destinations
                for conn in connections:
                    dest_ip = conn['remote_address']
                    if dest_ip:
                        if dest_ip not in destinations:
                            destinations[dest_ip] = {
                                'ip': dest_ip,
                                'ports': set(),
                                'connections': 0,
                                'processes': set()
                            }
                        destinations[dest_ip]['ports'].add(conn['remote_port'])
                        destinations[dest_ip]['connections'] += 1
                        destinations[dest_ip]['processes'].add(conn['process_name'])
                
                # Display current status
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                
                print(f"\r⏱️  [{elapsed:3d}s/{duration:3d}s] Connections: {total_connections:3d} | Destinations: {len(destinations):3d}", end="", flush=True)
                
                time.sleep(2)
            
            print(f"\n\n📊 {app_name.upper()} MONITORING COMPLETED")
            print("=" * 50)
            
            # Display results
            print(f"⏱️  Duration: {duration} seconds")
            print(f"🔗 Total Connections: {total_connections}")
            print(f"🌍 Unique Destinations: {len(destinations)}")
            
            if destinations:
                print(f"\n📍 DESTINATIONS DISCOVERED:")
                for dest_ip, info in destinations.items():
                    ports_str = ", ".join(map(str, info['ports']))
                    processes_str = ", ".join(info['processes'])
                    print(f"   • {dest_ip}")
                    print(f"     Ports: {ports_str}")
                    print(f"     Connections: {info['connections']}")
                    print(f"     Processes: {processes_str}")
                    print()
            
            # Save results to file
            results_file = f"logs/{app_name}_monitoring_{int(start_time)}.json"
            import json
            results = {
                'app_name': app_name,
                'start_time': start_time,
                'duration': duration,
                'total_connections': total_connections,
                'destinations': {ip: {**info, 'ports': list(info['ports']), 'processes': list(info['processes'])} 
                               for ip, info in destinations.items()}
            }
            
            Path("logs").mkdir(exist_ok=True)
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"💾 Results saved to: {results_file}")
            
        except KeyboardInterrupt:
            print(f"\n⏹️  {app_name} monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error monitoring {app_name}: {e}")
            print(f"❌ Error: {e}")
    
    def show_stats(self):
        """Show monitoring statistics"""
        try:
            if not self.network_monitor:
                self.network_monitor = NetworkMonitor()
            
            stats = self.db_manager.get_connection_stats(24)
            monitoring_stats = self.network_monitor.get_monitoring_stats()
            
            print("\n" + "="*50)
            print("NETWORK MONITOR STATISTICS")
            print("="*50)
            print(f"Monitoring Status: {'Running' if monitoring_stats['is_monitoring'] else 'Stopped'}")
            print(f"Interface: {monitoring_stats['interface']}")
            print(f"Local IP: {monitoring_stats['local_ip']}")
            print(f"Total Connections (24h): {stats.get('total_connections', 0)}")
            print(f"Unique Domains (24h): {stats.get('unique_domains', 0)}")
            print(f"Data Transferred (24h): {stats.get('total_data_mb', 0)} MB")
            print(f"Suspicious Connections (24h): {stats.get('suspicious_connections', 0)}")
            print("="*50)
            
            # Show top domains
            top_domains = self.db_manager.get_top_domains(5)
            if top_domains:
                print("\nTOP 5 DOMAINS:")
                for i, domain in enumerate(top_domains, 1):
                    print(f"{i}. {domain['dest_domain']} - {domain['access_count']} accesses")
            
            # Show recent alerts
            alerts = self.db_manager.get_recent_alerts(5)
            if alerts:
                print("\nRECENT ALERTS:")
                for alert in alerts:
                    print(f"- [{alert['severity']}] {alert['alert_type']}: {alert['message']}")
            
        except Exception as e:
            self.logger.error(f"Error showing stats: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Received shutdown signal, stopping monitoring...")
        self.stop_monitoring()
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Network Monitor - Monitor network traffic and destinations')
    parser.add_argument('--interface', '-i', default='eth0', help='Network interface to monitor')
    parser.add_argument('--dashboard', '-d', action='store_true', help='Run web dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Dashboard host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Dashboard port (default: 5000)')
    parser.add_argument('--stats', '-s', action='store_true', help='Show statistics and exit')
    parser.add_argument('--monitor-only', '-m', action='store_true', help='Run monitoring only (no dashboard)')
    parser.add_argument('--app-monitor', '-a', type=str, help='Monitor specific application (e.g., discord, chrome, firefox)')
    parser.add_argument('--app-duration', type=int, default=300, help='Duration for app monitoring in seconds')
    
    args = parser.parse_args()
    
    # Create app instance
    app_instance = NetworkMonitorApp()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, app_instance.signal_handler)
    signal.signal(signal.SIGTERM, app_instance.signal_handler)
    
    try:
        if args.stats:
            # Show statistics and exit
            app_instance.show_stats()
            return
        
        if args.dashboard:
            # Run dashboard only
            app_instance.run_dashboard(args.host, args.port)
        elif args.app_monitor:
            # Monitor specific application
            app_instance.monitor_application(args.app_monitor, args.app_duration)
        elif args.monitor_only:
            # Run monitoring only
            if app_instance.start_monitoring(args.interface):
                print(f"Network monitoring started on interface {args.interface}")
                print("Press Ctrl+C to stop...")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    app_instance.stop_monitoring()
        else:
            # Run both monitoring and dashboard
            if app_instance.start_monitoring(args.interface):
                print(f"Network monitoring started on interface {args.interface}")
                print(f"Starting web dashboard on {args.host}:{args.port}")
                print("Access dashboard at: http://localhost:5000")
                app_instance.run_dashboard(args.host, args.port)
    
    except KeyboardInterrupt:
        app_instance.stop_monitoring()
        print("\nApplication stopped by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
