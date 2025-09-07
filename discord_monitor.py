#!/usr/bin/env python3
"""
Discord Network Monitor
Monitor destinasi akses aplikasi Discord secara real-time
"""
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.monitor.process_monitor import ProcessMonitor
from src.utils.geo_utils import GeoLocationUtils

class DiscordMonitor:
    def __init__(self):
        self.process_monitor = ProcessMonitor()
        self.geo_utils = GeoLocationUtils()
        self.log_file = Path("logs/discord_monitor.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
    def log_message(self, message: str):
        """Log pesan ke file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        print(f"[{timestamp}] {message}")
    
    def check_discord_running(self) -> bool:
        """Cek apakah Discord sedang berjalan"""
        discord_processes = self.process_monitor.get_discord_processes()
        return len(discord_processes) > 0
    
    def monitor_discord_continuously(self, interval: int = 10):
        """Monitor Discord secara kontinyu"""
        self.log_message("🚀 Starting Discord Network Monitor...")
        
        if not self.check_discord_running():
            self.log_message("❌ Discord tidak ditemukan. Pastikan Discord sedang berjalan.")
            return
        
        self.log_message("✅ Discord ditemukan! Memulai monitoring...")
        
        try:
            while True:
                # Get Discord processes
                discord_processes = self.process_monitor.get_discord_processes()
                self.log_message(f"📊 Discord Processes: {len(discord_processes)}")
                
                for proc in discord_processes:
                    self.log_message(f"   - PID {proc['pid']}: {proc['name']}")
                
                # Get Discord connections
                discord_connections = self.process_monitor.get_discord_connections()
                self.log_message(f"🔗 Discord Connections: {len(discord_connections)}")
                
                # Analyze destinations
                destinations = {}
                for conn in discord_connections:
                    dest_ip = conn['remote_address']
                    if dest_ip:
                        if dest_ip not in destinations:
                            destinations[dest_ip] = {
                                'ip': dest_ip,
                                'ports': set(),
                                'connections': 0,
                                'country': self.geo_utils.get_country(dest_ip)
                            }
                        destinations[dest_ip]['ports'].add(conn['remote_port'])
                        destinations[dest_ip]['connections'] += 1
                
                # Display destinations
                if destinations:
                    self.log_message("🌍 Discord Destinations:")
                    for dest_ip, info in destinations.items():
                        ports_str = ", ".join(map(str, info['ports']))
                        self.log_message(f"   📍 {dest_ip} ({info['country']}) - Ports: {ports_str} - Connections: {info['connections']}")
                else:
                    self.log_message("   No active connections found")
                
                # Get detailed analysis
                analysis = self.process_monitor.get_discord_destinations_analysis()
                self.log_message(f"📈 Analysis: {analysis['total_destinations']} unique destinations")
                
                self.log_message("-" * 60)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log_message("⏹️  Monitoring stopped by user")
        except Exception as e:
            self.log_message(f"❌ Error: {e}")
    
    def monitor_discord_session(self, duration: int = 300):
        """Monitor Discord untuk sesi tertentu"""
        self.log_message(f"🎯 Starting Discord session monitoring for {duration} seconds...")
        
        if not self.check_discord_running():
            self.log_message("❌ Discord tidak ditemukan. Pastikan Discord sedang berjalan.")
            return
        
        start_time = datetime.now()
        session_data = {
            'start_time': start_time.isoformat(),
            'duration': duration,
            'destinations': {},
            'connections_log': [],
            'processes_log': []
        }
        
        end_time = start_time.timestamp() + duration
        
        try:
            while datetime.now().timestamp() < end_time:
                # Get current data
                discord_processes = self.process_monitor.get_discord_processes()
                discord_connections = self.process_monitor.get_discord_connections()
                
                # Log processes
                session_data['processes_log'].append({
                    'timestamp': datetime.now().isoformat(),
                    'processes': discord_processes
                })
                
                # Log connections
                session_data['connections_log'].append({
                    'timestamp': datetime.now().isoformat(),
                    'connections': discord_connections
                })
                
                # Update destinations
                for conn in discord_connections:
                    dest_ip = conn['remote_address']
                    if dest_ip:
                        if dest_ip not in session_data['destinations']:
                            session_data['destinations'][dest_ip] = {
                                'ip': dest_ip,
                                'country': self.geo_utils.get_country(dest_ip),
                                'ports': set(),
                                'total_connections': 0,
                                'first_seen': datetime.now().isoformat(),
                                'last_seen': datetime.now().isoformat()
                            }
                        
                        session_data['destinations'][dest_ip]['ports'].add(conn['remote_port'])
                        session_data['destinations'][dest_ip]['total_connections'] += 1
                        session_data['destinations'][dest_ip]['last_seen'] = datetime.now().isoformat()
                
                self.log_message(f"📊 Session Progress: {len(discord_connections)} connections, {len(session_data['destinations'])} destinations")
                time.sleep(5)
        
        except KeyboardInterrupt:
            self.log_message("⏹️  Session monitoring stopped by user")
        
        # Finalize session data
        session_data['end_time'] = datetime.now().isoformat()
        
        # Convert sets to lists
        for dest in session_data['destinations'].values():
            dest['ports'] = list(dest['ports'])
        
        # Save session data
        session_file = Path(f"logs/discord_session_{start_time.strftime('%Y%m%d_%H%M%S')}.json")
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self.log_message(f"💾 Session data saved to: {session_file}")
        
        # Display summary
        self.display_session_summary(session_data)
    
    def display_session_summary(self, session_data: dict):
        """Tampilkan ringkasan sesi monitoring"""
        self.log_message("=" * 60)
        self.log_message("📋 DISCORD MONITORING SESSION SUMMARY")
        self.log_message("=" * 60)
        
        duration = session_data['duration']
        destinations = session_data['destinations']
        
        self.log_message(f"⏱️  Duration: {duration} seconds")
        self.log_message(f"🌍 Total Destinations: {len(destinations)}")
        self.log_message(f"🔗 Total Connection Logs: {len(session_data['connections_log'])}")
        
        if destinations:
            self.log_message("\n📍 DESTINATIONS DISCOVERED:")
            for dest_ip, info in destinations.items():
                ports_str = ", ".join(map(str, info['ports']))
                self.log_message(f"   • {dest_ip} ({info['country']})")
                self.log_message(f"     Ports: {ports_str}")
                self.log_message(f"     Connections: {info['total_connections']}")
                self.log_message(f"     First Seen: {info['first_seen']}")
                self.log_message(f"     Last Seen: {info['last_seen']}")
                self.log_message("")
        
        self.log_message("=" * 60)
    
    def show_current_discord_status(self):
        """Tampilkan status Discord saat ini"""
        self.log_message("🔍 Current Discord Status:")
        
        if not self.check_discord_running():
            self.log_message("❌ Discord tidak berjalan")
            return
        
        # Get processes
        discord_processes = self.process_monitor.get_discord_processes()
        self.log_message(f"✅ Discord berjalan ({len(discord_processes)} processes)")
        
        for proc in discord_processes:
            self.log_message(f"   PID {proc['pid']}: {proc['name']}")
        
        # Get connections
        discord_connections = self.process_monitor.get_discord_connections()
        self.log_message(f"🔗 Active Connections: {len(discord_connections)}")
        
        if discord_connections:
            for conn in discord_connections:
                country = self.geo_utils.get_country(conn['remote_address'])
                self.log_message(f"   {conn['local_address']}:{conn['local_port']} -> {conn['remote_address']}:{conn['remote_port']} ({country})")
        
        # Get analysis
        analysis = self.process_monitor.get_discord_destinations_analysis()
        self.log_message(f"📊 Unique Destinations: {analysis['total_destinations']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Discord Network Monitor')
    parser.add_argument('--continuous', '-c', action='store_true', help='Monitor continuously')
    parser.add_argument('--session', '-s', type=int, default=300, help='Monitor for specific duration (seconds)')
    parser.add_argument('--status', action='store_true', help='Show current Discord status')
    parser.add_argument('--interval', '-i', type=int, default=10, help='Update interval for continuous monitoring (seconds)')
    
    args = parser.parse_args()
    
    monitor = DiscordMonitor()
    
    try:
        if args.status:
            monitor.show_current_discord_status()
        elif args.continuous:
            monitor.monitor_discord_continuously(args.interval)
        else:
            monitor.monitor_discord_session(args.session)
    
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
