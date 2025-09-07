#!/usr/bin/env python3
"""
Custom Application Monitor
Monitor aplikasi apapun dengan nama proses yang fleksibel
"""
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.monitor.process_monitor import ProcessMonitor
from src.utils.geo_utils import GeoLocationUtils

class CustomAppMonitor:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.process_monitor = ProcessMonitor()
        self.geo_utils = GeoLocationUtils()
        self.log_file = Path(f"logs/{app_name}_monitor.log")
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_message(self, message: str):
        """Log pesan ke file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        print(f"[{timestamp}] {message}")
    
    def find_app_processes(self):
        """Temukan proses aplikasi dengan berbagai nama"""
        possible_names = [
            self.app_name,
            self.app_name.lower(),
            self.app_name.upper(),
            f"{self.app_name}.exe",
            f"{self.app_name}.app",
            f"{self.app_name}-bin",
            f"{self.app_name}_bin"
        ]
        
        all_processes = []
        found_names = set()
        
        for name in possible_names:
            processes = self.process_monitor.get_process_by_name(name)
            for proc in processes:
                if proc['pid'] not in [p['pid'] for p in all_processes]:
                    all_processes.append(proc)
                    found_names.add(proc['name'])
        
        return all_processes, found_names
    
    def get_app_connections(self, processes):
        """Dapatkan koneksi untuk aplikasi"""
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
                        'local_port': conn['local_port'],
                        'status': conn['status'],
                        'timestamp': datetime.now().isoformat()
                    })
        
        return connections
    
    def monitor_app_continuous(self, interval: int = 10):
        """Monitor aplikasi secara kontinyu"""
        self.log_message(f"🚀 Starting continuous monitoring for {self.app_name}")
        
        processes, found_names = self.find_app_processes()
        if not processes:
            self.log_message(f"❌ {self.app_name} tidak ditemukan")
            self.log_message("💡 Coba nama proses yang berbeda:")
            self.log_message("   - Cek dengan: ps aux | grep -i 'nama_aplikasi'")
            self.log_message("   - Cek dengan: netstat -tulpn | grep 'nama_aplikasi'")
            return
        
        self.log_message(f"✅ {self.app_name} ditemukan! ({len(processes)} processes)")
        self.log_message(f"📋 Process names: {', '.join(found_names)}")
        
        for proc in processes:
            self.log_message(f"   PID {proc['pid']}: {proc['name']}")
        
        try:
            while True:
                connections = self.get_app_connections(processes)
                self.log_message(f"🔗 Active Connections: {len(connections)}")
                
                if connections:
                    # Group by destination
                    destinations = {}
                    for conn in connections:
                        dest_ip = conn['remote_address']
                        if dest_ip not in destinations:
                            destinations[dest_ip] = {
                                'ip': dest_ip,
                                'country': self.geo_utils.get_country(dest_ip),
                                'ports': set(),
                                'connections': 0,
                                'processes': set()
                            }
                        destinations[dest_ip]['ports'].add(conn['remote_port'])
                        destinations[dest_ip]['connections'] += 1
                        destinations[dest_ip]['processes'].add(conn['process_name'])
                    
                    # Display destinations
                    self.log_message(f"🌍 Destinations: {len(destinations)}")
                    for dest_ip, info in list(destinations.items())[:5]:  # Show top 5
                        ports_str = ", ".join(map(str, info['ports']))
                        self.log_message(f"   📍 {dest_ip} ({info['country']}) - Ports: {ports_str} - Connections: {info['connections']}")
                else:
                    self.log_message("   No active connections found")
                
                self.log_message("-" * 60)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log_message("⏹️  Monitoring stopped by user")
        except Exception as e:
            self.log_message(f"❌ Error: {e}")
    
    def monitor_app_session(self, duration: int = 300):
        """Monitor aplikasi untuk sesi tertentu"""
        self.log_message(f"🎯 Starting {self.app_name} session monitoring for {duration} seconds")
        
        processes, found_names = self.find_app_processes()
        if not processes:
            self.log_message(f"❌ {self.app_name} tidak ditemukan")
            return
        
        self.log_message(f"✅ {self.app_name} ditemukan! ({len(processes)} processes)")
        self.log_message(f"📋 Process names: {', '.join(found_names)}")
        
        start_time = datetime.now()
        session_data = {
            'app_name': self.app_name,
            'start_time': start_time.isoformat(),
            'duration': duration,
            'processes': processes,
            'destinations': {},
            'connections_log': [],
            'processes_found': list(found_names)
        }
        
        end_time = start_time.timestamp() + duration
        
        try:
            while datetime.now().timestamp() < end_time:
                connections = self.get_app_connections(processes)
                
                # Log connections
                session_data['connections_log'].append({
                    'timestamp': datetime.now().isoformat(),
                    'connections': connections
                })
                
                # Update destinations
                for conn in connections:
                    dest_ip = conn['remote_address']
                    if dest_ip:
                        if dest_ip not in session_data['destinations']:
                            session_data['destinations'][dest_ip] = {
                                'ip': dest_ip,
                                'country': self.geo_utils.get_country(dest_ip),
                                'ports': set(),
                                'total_connections': 0,
                                'first_seen': datetime.now().isoformat(),
                                'last_seen': datetime.now().isoformat(),
                                'processes': set()
                            }
                        
                        session_data['destinations'][dest_ip]['ports'].add(conn['remote_port'])
                        session_data['destinations'][dest_ip]['total_connections'] += 1
                        session_data['destinations'][dest_ip]['last_seen'] = datetime.now().isoformat()
                        session_data['destinations'][dest_ip]['processes'].add(conn['process_name'])
                
                elapsed = int(datetime.now().timestamp() - start_time.timestamp())
                remaining = duration - elapsed
                
                print(f"\r⏱️  [{elapsed:3d}s/{duration:3d}s] Connections: {len(connections):3d} | Destinations: {len(session_data['destinations']):3d}", end="", flush=True)
                time.sleep(2)
        
        except KeyboardInterrupt:
            self.log_message("⏹️  Session monitoring stopped by user")
        
        # Finalize session data
        session_data['end_time'] = datetime.now().isoformat()
        
        # Convert sets to lists
        for dest in session_data['destinations'].values():
            dest['ports'] = list(dest['ports'])
            dest['processes'] = list(dest['processes'])
        
        # Save session data
        session_file = Path(f"logs/{self.app_name}_session_{start_time.strftime('%Y%m%d_%H%M%S')}.json")
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self.log_message(f"💾 Session data saved to: {session_file}")
        
        # Display summary
        self.display_session_summary(session_data)
    
    def display_session_summary(self, session_data: dict):
        """Tampilkan ringkasan sesi monitoring"""
        self.log_message("=" * 60)
        self.log_message(f"📋 {self.app_name.upper()} MONITORING SESSION SUMMARY")
        self.log_message("=" * 60)
        
        duration = session_data['duration']
        destinations = session_data['destinations']
        
        self.log_message(f"⏱️  Duration: {duration} seconds")
        self.log_message(f"🌍 Total Destinations: {len(destinations)}")
        self.log_message(f"🔗 Total Connection Logs: {len(session_data['connections_log'])}")
        self.log_message(f"📋 Processes Found: {', '.join(session_data['processes_found'])}")
        
        if destinations:
            self.log_message("\n📍 DESTINATIONS DISCOVERED:")
            for dest_ip, info in destinations.items():
                ports_str = ", ".join(map(str, info['ports']))
                processes_str = ", ".join(info['processes'])
                self.log_message(f"   • {dest_ip} ({info['country']})")
                self.log_message(f"     Ports: {ports_str}")
                self.log_message(f"     Connections: {info['total_connections']}")
                self.log_message(f"     Processes: {processes_str}")
                self.log_message(f"     First Seen: {info['first_seen']}")
                self.log_message(f"     Last Seen: {info['last_seen']}")
                self.log_message("")
        
        self.log_message("=" * 60)
    
    def show_app_status(self):
        """Tampilkan status aplikasi saat ini"""
        self.log_message(f"🔍 Current {self.app_name} Status:")
        
        processes, found_names = self.find_app_processes()
        if not processes:
            self.log_message(f"❌ {self.app_name} tidak berjalan")
            return
        
        self.log_message(f"✅ {self.app_name} berjalan ({len(processes)} processes)")
        self.log_message(f"📋 Process names: {', '.join(found_names)}")
        
        for proc in processes:
            self.log_message(f"   PID {proc['pid']}: {proc['name']}")
        
        # Get connections
        connections = self.get_app_connections(processes)
        self.log_message(f"🔗 Active Connections: {len(connections)}")
        
        if connections:
            # Group by destination
            destinations = {}
            for conn in connections:
                dest_ip = conn['remote_address']
                if dest_ip not in destinations:
                    destinations[dest_ip] = {
                        'ip': dest_ip,
                        'country': self.geo_utils.get_country(dest_ip),
                        'ports': set(),
                        'connections': 0
                    }
                destinations[dest_ip]['ports'].add(conn['remote_port'])
                destinations[dest_ip]['connections'] += 1
            
            self.log_message(f"🌍 Unique Destinations: {len(destinations)}")
            for dest_ip, info in destinations.items():
                ports_str = ", ".join(map(str, info['ports']))
                self.log_message(f"   {dest_ip} ({info['country']}) - Ports: {ports_str} - Connections: {info['connections']}")

def main():
    parser = argparse.ArgumentParser(description='Custom Application Monitor')
    parser.add_argument('app_name', help='Name of application to monitor')
    parser.add_argument('--continuous', '-c', action='store_true', help='Monitor continuously')
    parser.add_argument('--session', '-s', type=int, default=300, help='Monitor for specific duration (seconds)')
    parser.add_argument('--status', action='store_true', help='Show current application status')
    parser.add_argument('--interval', '-i', type=int, default=10, help='Update interval for continuous monitoring (seconds)')
    
    args = parser.parse_args()
    
    monitor = CustomAppMonitor(args.app_name)
    
    try:
        if args.status:
            monitor.show_app_status()
        elif args.continuous:
            monitor.monitor_app_continuous(args.interval)
        else:
            monitor.monitor_app_session(args.session)
    
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
