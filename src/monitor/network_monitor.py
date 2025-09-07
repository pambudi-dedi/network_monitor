"""
Network Monitor - Modul utama untuk monitoring traffic jaringan
"""
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional
import socket
import struct
import psutil
import netifaces

try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.layers.dns import DNS
except ImportError:
    print("Scapy tidak terinstall. Jalankan: pip install scapy")
    exit(1)

from config.config import MONITORING_CONFIG, FILTERED_DOMAINS, ALERT_THRESHOLDS
from src.database.db_manager import DatabaseManager
from src.utils.geo_utils import GeoLocationUtils

class NetworkMonitor:
    def __init__(self, interface: str = None):
        self.interface = interface or MONITORING_CONFIG['interface']
        self.db_manager = DatabaseManager()
        self.geo_utils = GeoLocationUtils()
        self.logger = logging.getLogger(__name__)
        self.is_monitoring = False
        self.monitor_thread = None
        self.connection_count = 0
        self.connections_per_minute = {}
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/monitor.log'),
                logging.StreamHandler()
            ]
        )
    
    def get_network_interfaces(self) -> List[str]:
        """Dapatkan daftar network interface yang tersedia"""
        try:
            interfaces = netifaces.interfaces()
            return [iface for iface in interfaces if iface != 'lo']
        except Exception as e:
            self.logger.error(f"Error getting network interfaces: {e}")
            return []
    
    def resolve_domain(self, ip_address: str) -> Optional[str]:
        """Resolve IP address ke domain name"""
        try:
            if ip_address in FILTERED_DOMAINS:
                return None
                
            # Coba reverse DNS lookup
            domain = socket.gethostbyaddr(ip_address)[0]
            return domain if domain != ip_address else None
        except:
            return None
    
    def is_suspicious_connection(self, dest_ip: str, dest_port: int, protocol: str) -> bool:
        """Cek apakah koneksi mencurigakan"""
        try:
            # Cek port yang mencurigakan
            suspicious_ports = [22, 23, 135, 139, 445, 1433, 3389, 5900]
            if dest_port in suspicious_ports:
                return True
            
            # Cek IP private yang tidak seharusnya diakses dari luar
            if dest_ip.startswith('192.168.') or dest_ip.startswith('10.'):
                return False
                
            # Cek domain yang mencurigakan
            domain = self.resolve_domain(dest_ip)
            if domain and any(susp in domain.lower() for susp in ALERT_THRESHOLDS['suspicious_domains']):
                return True
                
            return False
        except:
            return False
    
    def process_packet(self, packet):
        """Process setiap packet yang ditangkap"""
        try:
            if not packet.haslayer(IP):
                return
            
            ip_layer = packet[IP]
            source_ip = ip_layer.src
            dest_ip = ip_layer.dst
            protocol = ip_layer.proto
            
            # Skip traffic internal
            if source_ip in FILTERED_DOMAINS or dest_ip in FILTERED_DOMAINS:
                return
            
            # Extract port information
            dest_port = None
            if packet.haslayer(TCP):
                dest_port = packet[TCP].dport
                protocol_name = "TCP"
            elif packet.haslayer(UDP):
                dest_port = packet[UDP].dport
                protocol_name = "UDP"
            else:
                protocol_name = "OTHER"
            
            # Resolve domain
            dest_domain = self.resolve_domain(dest_ip)
            
            # Cek apakah mencurigakan
            is_suspicious = self.is_suspicious_connection(dest_ip, dest_port, protocol_name)
            
            # Get country information
            country = self.geo_utils.get_country(dest_ip)
            
            # Prepare connection data
            connection_data = {
                'source_ip': source_ip,
                'dest_ip': dest_ip,
                'dest_port': dest_port,
                'protocol': protocol_name,
                'dest_domain': dest_domain,
                'packet_size': len(packet),
                'connection_type': 'OUTBOUND' if source_ip != self.get_local_ip() else 'INBOUND',
                'country': country,
                'is_suspicious': is_suspicious,
                'raw_data': {
                    'timestamp': datetime.now().isoformat(),
                    'packet_summary': packet.summary()
                }
            }
            
            # Simpan ke database
            self.db_manager.insert_connection(connection_data)
            
            # Update connection count
            self.connection_count += 1
            current_minute = int(time.time() / 60)
            self.connections_per_minute[current_minute] = self.connections_per_minute.get(current_minute, 0) + 1
            
            # Cek threshold alert
            if self.connections_per_minute[current_minute] > ALERT_THRESHOLDS['max_connections_per_minute']:
                self.db_manager.insert_alert(
                    'HIGH_TRAFFIC',
                    f'High traffic detected: {self.connections_per_minute[current_minute]} connections in last minute',
                    'WARNING'
                )
            
            # Log suspicious connections
            if is_suspicious:
                self.logger.warning(f"Suspicious connection detected: {source_ip} -> {dest_ip}:{dest_port}")
                self.db_manager.insert_alert(
                    'SUSPICIOUS_CONNECTION',
                    f'Suspicious connection: {source_ip} -> {dest_ip}:{dest_port} ({dest_domain or "Unknown"})',
                    'CRITICAL'
                )
            
            # Log setiap 100 koneksi
            if self.connection_count % 100 == 0:
                self.logger.info(f"Processed {self.connection_count} connections")
                
        except Exception as e:
            self.logger.error(f"Error processing packet: {e}")
    
    def get_local_ip(self) -> str:
        """Dapatkan IP lokal"""
        try:
            # Coba dapatkan IP dari interface yang sedang digunakan
            addrs = netifaces.ifaddresses(self.interface)
            if netifaces.AF_INET in addrs:
                return addrs[netifaces.AF_INET][0]['addr']
            
            # Fallback ke method lain
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def start_monitoring(self):
        """Mulai monitoring network traffic"""
        if self.is_monitoring:
            self.logger.warning("Monitoring sudah berjalan")
            return
        
        self.logger.info(f"Starting network monitoring on interface: {self.interface}")
        self.is_monitoring = True
        
        # Start monitoring in separate thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        """Loop monitoring utama"""
        try:
            # Sniff packets
            sniff(
                iface=self.interface,
                prn=self.process_packet,
                timeout=MONITORING_CONFIG['capture_timeout'],
                count=MONITORING_CONFIG['max_packets']
            )
        except Exception as e:
            self.logger.error(f"Error in monitoring loop: {e}")
        finally:
            self.is_monitoring = False
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.logger.info("Stopping network monitoring...")
        self.is_monitoring = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
    
    def get_monitoring_stats(self) -> Dict:
        """Dapatkan statistik monitoring"""
        return {
            'is_monitoring': self.is_monitoring,
            'total_connections': self.connection_count,
            'connections_per_minute': dict(self.connections_per_minute),
            'interface': self.interface,
            'local_ip': self.get_local_ip()
        }
    
    def get_network_info(self) -> Dict:
        """Dapatkan informasi network interface"""
        try:
            interfaces = self.get_network_interfaces()
            interface_info = {}
            
            for iface in interfaces:
                try:
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        ip_info = addrs[netifaces.AF_INET][0]
                        interface_info[iface] = {
                            'ip': ip_info.get('addr'),
                            'netmask': ip_info.get('netmask'),
                            'broadcast': ip_info.get('broadcast')
                        }
                except:
                    continue
            
            return {
                'available_interfaces': interfaces,
                'current_interface': self.interface,
                'interface_details': interface_info
            }
        except Exception as e:
            self.logger.error(f"Error getting network info: {e}")
            return {}
