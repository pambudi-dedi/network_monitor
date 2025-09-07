"""
Utility untuk geolocation dan IP information
"""
import requests
import logging
from typing import Optional, Dict
import time

class GeoLocationUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour cache
        
    def get_country(self, ip_address: str) -> Optional[str]:
        """Dapatkan negara dari IP address"""
        try:
            # Skip private IPs
            if self._is_private_ip(ip_address):
                return "Private"
            
            # Check cache first
            if ip_address in self.cache:
                cached_data = self.cache[ip_address]
                if time.time() - cached_data['timestamp'] < self.cache_timeout:
                    return cached_data['country']
            
            # Use ip-api.com (free service)
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', 'Unknown')
                
                # Cache the result
                self.cache[ip_address] = {
                    'country': country,
                    'timestamp': time.time()
                }
                
                return country
            
        except Exception as e:
            self.logger.error(f"Error getting country for {ip_address}: {e}")
        
        return "Unknown"
    
    def get_ip_info(self, ip_address: str) -> Dict:
        """Dapatkan informasi lengkap IP address"""
        try:
            if self._is_private_ip(ip_address):
                return {
                    'ip': ip_address,
                    'country': 'Private',
                    'region': 'Private',
                    'city': 'Private',
                    'isp': 'Private',
                    'org': 'Private'
                }
            
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'ip': data.get('query', ip_address),
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone', 'Unknown')
                }
        except Exception as e:
            self.logger.error(f"Error getting IP info for {ip_address}: {e}")
        
        return {
            'ip': ip_address,
            'country': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'isp': 'Unknown',
            'org': 'Unknown'
        }
    
    def _is_private_ip(self, ip_address: str) -> bool:
        """Cek apakah IP address adalah private IP"""
        try:
            import ipaddress
            ip = ipaddress.ip_address(ip_address)
            return ip.is_private
        except:
            # Fallback untuk IP yang tidak valid
            return ip_address.startswith('192.168.') or \
                   ip_address.startswith('10.') or \
                   ip_address.startswith('172.') or \
                   ip_address == '127.0.0.1'
    
    def get_my_ip(self) -> str:
        """Dapatkan IP publik sendiri"""
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except Exception as e:
            self.logger.error(f"Error getting public IP: {e}")
        
        return "Unknown"
