# 🎯 Specific Application Monitoring Guide

## 📱 Monitoring Aplikasi Spesifik

Network Monitor dapat memonitor aplikasi apapun yang memiliki koneksi jaringan. Berikut panduan lengkap untuk berbagai jenis aplikasi.

## 🔍 Cara Menemukan Nama Proses Aplikasi

### 1. Cek Proses yang Berjalan
```bash
# Lihat semua proses
ps aux | grep -i "nama_aplikasi"

# Contoh untuk Discord
ps aux | grep -i discord

# Contoh untuk Chrome
ps aux | grep -i chrome

# Contoh untuk Steam
ps aux | grep -i steam
```

### 2. Cek dengan Network Connections
```bash
# Lihat proses dengan koneksi jaringan
netstat -tulpn | grep "nama_aplikasi"

# Atau gunakan ss
ss -tulpn | grep "nama_aplikasi"
```

### 3. Cek dengan lsof
```bash
# Lihat file dan koneksi yang dibuka aplikasi
lsof -i -P | grep "nama_aplikasi"
```

## 🎮 Gaming Applications

### Steam
```bash
# Monitor Steam
python3 main.py --app-monitor steam --app-duration 300

# Jika nama proses berbeda
python3 main.py --app-monitor "steam.exe" --app-duration 300
python3 main.py --app-monitor "steamwebhelper" --app-duration 300
```

### Epic Games Launcher
```bash
# Monitor Epic Games
python3 main.py --app-monitor epic --app-duration 300
python3 main.py --app-monitor "EpicGamesLauncher" --app-duration 300
```

### Battle.net (Blizzard)
```bash
# Monitor Battle.net
python3 main.py --app-monitor battle --app-duration 300
python3 main.py --app-monitor "Battle.net" --app-duration 300
```

### Origin (EA)
```bash
# Monitor Origin
python3 main.py --app-monitor origin --app-duration 300
python3 main.py --app-monitor "Origin.exe" --app-duration 300
```

## 🌐 Web Browsers

### Google Chrome
```bash
# Monitor Chrome
python3 main.py --app-monitor chrome --app-duration 300

# Monitor Chrome dengan nama proses spesifik
python3 main.py --app-monitor "chrome.exe" --app-duration 300
python3 main.py --app-monitor "chrome_crashpad_handler" --app-duration 300
```

### Mozilla Firefox
```bash
# Monitor Firefox
python3 main.py --app-monitor firefox --app-duration 300
python3 main.py --app-monitor "firefox-esr" --app-duration 300
```

### Microsoft Edge
```bash
# Monitor Edge
python3 main.py --app-monitor edge --app-duration 300
python3 main.py --app-monitor "msedge.exe" --app-duration 300
```

### Safari
```bash
# Monitor Safari
python3 main.py --app-monitor safari --app-duration 300
python3 main.py --app-monitor "Safari.app" --app-duration 300
```

## 🎵 Media Applications

### Spotify
```bash
# Monitor Spotify
python3 main.py --app-monitor spotify --app-duration 300
python3 main.py --app-monitor "Spotify.exe" --app-duration 300
```

### YouTube Music
```bash
# Monitor YouTube Music
python3 main.py --app-monitor "youtube-music" --app-duration 300
```

### VLC Media Player
```bash
# Monitor VLC
python3 main.py --app-monitor vlc --app-duration 300
python3 main.py --app-monitor "vlc.exe" --app-duration 300
```

## 💻 Development Tools

### Visual Studio Code
```bash
# Monitor VS Code
python3 main.py --app-monitor code --app-duration 300
python3 main.py --app-monitor "Code.exe" --app-duration 300
```

### Git
```bash
# Monitor Git operations
python3 main.py --app-monitor git --app-duration 300
```

### Docker
```bash
# Monitor Docker
python3 main.py --app-monitor docker --app-duration 300
python3 main.py --app-monitor "dockerd" --app-duration 300
```

### Node.js
```bash
# Monitor Node.js applications
python3 main.py --app-monitor node --app-duration 300
python3 main.py --app-monitor "node.exe" --app-duration 300
```

## 📧 Communication Apps

### Telegram
```bash
# Monitor Telegram
python3 main.py --app-monitor telegram --app-duration 300
python3 main.py --app-monitor "Telegram.exe" --app-duration 300
```

### WhatsApp Desktop
```bash
# Monitor WhatsApp
python3 main.py --app-monitor whatsapp --app-duration 300
python3 main.py --app-monitor "WhatsApp.exe" --app-duration 300
```

### Slack
```bash
# Monitor Slack
python3 main.py --app-monitor slack --app-duration 300
python3 main.py --app-monitor "Slack.exe" --app-duration 300
```

## 🛠️ Custom Application Monitoring

### 1. Buat Script Monitoring Kustom

```python
#!/usr/bin/env python3
"""
Custom Application Monitor
"""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.monitor.process_monitor import ProcessMonitor
from src.utils.geo_utils import GeoLocationUtils

class CustomAppMonitor:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.process_monitor = ProcessMonitor()
        self.geo_utils = GeoLocationUtils()
    
    def find_app_processes(self):
        """Temukan proses aplikasi dengan berbagai nama"""
        possible_names = [
            self.app_name,
            self.app_name.lower(),
            self.app_name.upper(),
            f"{self.app_name}.exe",
            f"{self.app_name}.app"
        ]
        
        all_processes = []
        for name in possible_names:
            processes = self.process_monitor.get_process_by_name(name)
            all_processes.extend(processes)
        
        return all_processes
    
    def monitor_app(self, duration: int = 300):
        """Monitor aplikasi kustom"""
        print(f"🎯 Monitoring {self.app_name.upper()}")
        print("=" * 50)
        
        # Find processes
        processes = self.find_app_processes()
        if not processes:
            print(f"❌ {self.app_name} tidak ditemukan")
            print("💡 Coba nama proses yang berbeda:")
            print("   - Cek dengan: ps aux | grep -i 'nama_aplikasi'")
            print("   - Cek dengan: netstat -tulpn | grep 'nama_aplikasi'")
            return
        
        print(f"✅ {self.app_name} ditemukan! ({len(processes)} processes)")
        for proc in processes:
            print(f"   PID {proc['pid']}: {proc['name']}")
        
        # Monitor connections
        start_time = time.time()
        destinations = {}
        
        while time.time() - start_time < duration:
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
            
            # Update destinations
            for conn in connections:
                dest_ip = conn['remote_address']
                if dest_ip:
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
            
            elapsed = int(time.time() - start_time)
            print(f"\r⏱️  [{elapsed:3d}s/{duration:3d}s] Connections: {len(connections):3d} | Destinations: {len(destinations):3d}", end="", flush=True)
            time.sleep(2)
        
        # Display results
        print(f"\n\n📊 {self.app_name.upper()} MONITORING COMPLETED")
        print("=" * 50)
        print(f"⏱️  Duration: {duration} seconds")
        print(f"🔗 Total Connections: {len(connections)}")
        print(f"🌍 Unique Destinations: {len(destinations)}")
        
        if destinations:
            print(f"\n📍 DESTINATIONS DISCOVERED:")
            for dest_ip, info in destinations.items():
                ports_str = ", ".join(map(str, info['ports']))
                processes_str = ", ".join(info['processes'])
                print(f"   • {dest_ip} ({info['country']})")
                print(f"     Ports: {ports_str}")
                print(f"     Connections: {info['connections']}")
                print(f"     Processes: {processes_str}")
                print()
        
        return destinations

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Custom Application Monitor')
    parser.add_argument('app_name', help='Name of application to monitor')
    parser.add_argument('--duration', '-d', type=int, default=300, help='Monitoring duration in seconds')
    
    args = parser.parse_args()
    
    monitor = CustomAppMonitor(args.app_name)
    monitor.monitor_app(args.duration)

if __name__ == '__main__':
    main()
```

### 2. Gunakan Script Kustom

```bash
# Monitor aplikasi kustom
python3 custom_app_monitor.py "nama_aplikasi" --duration 300

# Contoh
python3 custom_app_monitor.py "steam" --duration 300
python3 custom_app_monitor.py "spotify" --duration 300
python3 custom_app_monitor.py "telegram" --duration 300
```

## 🔧 Advanced Monitoring Techniques

### 1. Monitor Multiple Processes

```python
# Monitor semua proses yang mengandung kata kunci
def monitor_by_keyword(keyword: str):
    monitor = ProcessMonitor()
    processes = monitor.get_process_by_name(keyword)
    
    for proc in processes:
        print(f"Monitoring {proc['name']} (PID {proc['pid']})")
        connections = monitor._get_process_connections(proc['pid'])
        # Process connections...
```

### 2. Monitor by Port

```python
# Monitor aplikasi berdasarkan port yang digunakan
def monitor_by_port(port: int):
    import subprocess
    
    # Cari proses yang menggunakan port tertentu
    result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
    
    if result.stdout:
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                pid = parts[1]
                process_name = parts[0]
                print(f"Process {process_name} (PID {pid}) using port {port}")
```

### 3. Monitor by Network Interface

```python
# Monitor aplikasi berdasarkan interface jaringan
def monitor_by_interface(interface: str):
    # Implementasi monitoring berdasarkan interface
    pass
```

## 📊 Monitoring Specific Services

### 1. Database Connections
```bash
# Monitor MySQL
python3 main.py --app-monitor mysql --app-duration 300

# Monitor PostgreSQL
python3 main.py --app-monitor postgres --app-duration 300

# Monitor MongoDB
python3 main.py --app-monitor mongod --app-duration 300
```

### 2. Web Servers
```bash
# Monitor Apache
python3 main.py --app-monitor apache2 --app-duration 300

# Monitor Nginx
python3 main.py --app-monitor nginx --app-duration 300

# Monitor Node.js server
python3 main.py --app-monitor node --app-duration 300
```

### 3. Cloud Services
```bash
# Monitor AWS CLI
python3 main.py --app-monitor aws --app-duration 300

# Monitor Docker
python3 main.py --app-monitor docker --app-duration 300

# Monitor Kubernetes
python3 main.py --app-monitor kubectl --app-duration 300
```

## 🚨 Troubleshooting Specific Apps

### 1. Aplikasi Tidak Ditemukan
```bash
# Cek semua proses
ps aux | grep -i "nama_aplikasi"

# Cek dengan nama yang berbeda
python3 main.py --app-monitor "NamaAplikasi.exe" --app-duration 300

# Cek dengan path lengkap
python3 main.py --app-monitor "/path/to/app" --app-duration 300
```

### 2. Aplikasi Tidak Ada Koneksi
```bash
# Pastikan aplikasi sedang aktif
# Buka aplikasi dan gunakan fitur yang memerlukan internet

# Cek koneksi manual
netstat -tulpn | grep "nama_aplikasi"

# Cek dengan lsof
lsof -i -P | grep "nama_aplikasi"
```

### 3. Permission Issues
```bash
# Jalankan dengan sudo
sudo python3 main.py --app-monitor "nama_aplikasi" --app-duration 300

# Atau gunakan systemd service
sudo systemctl start network-monitor
```

## 📈 Best Practices

### 1. Monitoring Duration
```bash
# Untuk testing cepat
python3 main.py --app-monitor "nama_aplikasi" --app-duration 60

# Untuk monitoring normal
python3 main.py --app-monitor "nama_aplikasi" --app-duration 300

# Untuk monitoring panjang
python3 main.py --app-monitor "nama_aplikasi" --app-duration 3600
```

### 2. Multiple Apps Monitoring
```bash
# Terminal 1
python3 main.py --app-monitor discord --app-duration 600 &

# Terminal 2
python3 main.py --app-monitor chrome --app-duration 600 &

# Terminal 3
python3 main.py --app-monitor spotify --app-duration 600 &
```

### 3. Data Analysis
```python
# Analisis hasil monitoring
import json

with open('logs/discord_monitoring_1234567890.json', 'r') as f:
    data = json.load(f)

# Analisis destinasi
destinations = data['destinations']
for ip, info in destinations.items():
    print(f"IP: {ip}")
    print(f"Country: {info['country']}")
    print(f"Ports: {info['ports']}")
    print(f"Connections: {info['connections']}")
```

---

**Dengan panduan ini, Anda dapat memonitor aplikasi apapun yang memiliki koneksi jaringan!** 🚀
