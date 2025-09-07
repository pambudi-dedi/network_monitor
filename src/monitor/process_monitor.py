"""
Process-specific Network Monitor
Monitor network traffic untuk aplikasi spesifik seperti Discord
"""
import psutil
import logging
from typing import Dict, List, Set, Optional
from datetime import datetime
import subprocess
import re

class ProcessMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.process_cache = {}
        self.port_to_process = {}
        
    def get_process_by_name(self, process_name: str) -> List[Dict]:
        """Dapatkan proses berdasarkan nama aplikasi"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'connections']):
                try:
                    proc_info = proc.info
                    if process_name.lower() in proc_info['name'].lower():
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else '',
                            'connections': self._get_process_connections(proc_info['pid'])
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            self.logger.error(f"Error getting processes: {e}")
        
        return processes
    
    def _get_process_connections(self, pid: int) -> List[Dict]:
        """Dapatkan koneksi untuk proses tertentu"""
        connections = []
        try:
            proc = psutil.Process(pid)
            for conn in proc.connections():
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        'local_address': conn.laddr.ip if conn.laddr else None,
                        'local_port': conn.laddr.port if conn.laddr else None,
                        'remote_address': conn.raddr.ip if conn.raddr else None,
                        'remote_port': conn.raddr.port if conn.raddr else None,
                        'status': conn.status,
                        'family': conn.family.name if hasattr(conn.family, 'name') else str(conn.family)
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except Exception as e:
            self.logger.error(f"Error getting connections for PID {pid}: {e}")
        
        return connections
    
    def get_discord_processes(self) -> List[Dict]:
        """Dapatkan semua proses Discord yang berjalan"""
        discord_processes = []
        
        # Nama proses Discord yang mungkin
        discord_names = ['discord', 'Discord', 'Discord.exe', 'discord.exe']
        
        for name in discord_names:
            processes = self.get_process_by_name(name)
            discord_processes.extend(processes)
        
        return discord_processes
    
    def get_discord_connections(self) -> List[Dict]:
        """Dapatkan semua koneksi Discord"""
        discord_connections = []
        discord_processes = self.get_discord_processes()
        
        for proc in discord_processes:
            for conn in proc['connections']:
                if conn['remote_address'] and conn['remote_port']:
                    discord_connections.append({
                        'process_name': proc['name'],
                        'pid': proc['pid'],
                        'local_address': conn['local_address'],
                        'local_port': conn['local_port'],
                        'remote_address': conn['remote_address'],
                        'remote_port': conn['remote_port'],
                        'status': conn['status'],
                        'timestamp': datetime.now().isoformat()
                    })
        
        return discord_connections
    
    def monitor_discord_traffic(self, duration: int = 60) -> Dict:
        """Monitor traffic Discord untuk durasi tertentu"""
        self.logger.info(f"Starting Discord traffic monitoring for {duration} seconds...")
        
        start_time = datetime.now()
        discord_data = {
            'start_time': start_time.isoformat(),
            'duration': duration,
            'processes': [],
            'connections': [],
            'destinations': set(),
            'total_connections': 0
        }
        
        # Monitor setiap 5 detik
        import time
        end_time = start_time.timestamp() + duration
        
        while datetime.now().timestamp() < end_time:
            # Get Discord processes
            discord_processes = self.get_discord_processes()
            discord_data['processes'] = discord_processes
            
            # Get Discord connections
            discord_connections = self.get_discord_connections()
            discord_data['connections'] = discord_connections
            discord_data['total_connections'] = len(discord_connections)
            
            # Collect unique destinations
            for conn in discord_connections:
                if conn['remote_address']:
                    discord_data['destinations'].add(conn['remote_address'])
            
            self.logger.info(f"Discord monitoring: {len(discord_processes)} processes, {len(discord_connections)} connections")
            time.sleep(5)
        
        discord_data['end_time'] = datetime.now().isoformat()
        discord_data['destinations'] = list(discord_data['destinations'])
        
        return discord_data
    
    def get_network_stats_for_process(self, process_name: str) -> Dict:
        """Dapatkan statistik network untuk proses tertentu"""
        processes = self.get_process_by_name(process_name)
        
        total_connections = 0
        unique_destinations = set()
        ports_used = set()
        
        for proc in processes:
            connections = proc['connections']
            total_connections += len(connections)
            
            for conn in connections:
                if conn['remote_address']:
                    unique_destinations.add(conn['remote_address'])
                if conn['remote_port']:
                    ports_used.add(conn['remote_port'])
        
        return {
            'process_name': process_name,
            'process_count': len(processes),
            'total_connections': total_connections,
            'unique_destinations': len(unique_destinations),
            'destinations': list(unique_destinations),
            'ports_used': list(ports_used),
            'timestamp': datetime.now().isoformat()
        }
    
    def resolve_discord_domains(self, ip_addresses: List[str]) -> Dict[str, str]:
        """Resolve IP addresses ke domain names untuk Discord"""
        resolved_domains = {}
        
        for ip in ip_addresses:
            try:
                import socket
                domain = socket.gethostbyaddr(ip)[0]
                resolved_domains[ip] = domain
            except:
                resolved_domains[ip] = "Unknown"
        
        return resolved_domains
    
    def get_discord_destinations_analysis(self) -> Dict:
        """Analisis lengkap destinasi Discord"""
        discord_connections = self.get_discord_connections()
        
        # Group by destination
        destinations = {}
        for conn in discord_connections:
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
        
        # Convert sets to lists
        for dest in destinations.values():
            dest['ports'] = list(dest['ports'])
            dest['processes'] = list(dest['processes'])
        
        # Resolve domains
        ip_list = list(destinations.keys())
        resolved_domains = self.resolve_discord_domains(ip_list)
        
        # Add domain info
        for dest in destinations.values():
            dest['domain'] = resolved_domains.get(dest['ip'], 'Unknown')
        
        return {
            'total_destinations': len(destinations),
            'destinations': destinations,
            'analysis_time': datetime.now().isoformat()
        }
