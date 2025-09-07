# 🎯 Complete Application Monitoring Guide

## 📋 Panduan Lengkap Monitoring Aplikasi Spesifik

Network Monitor mendukung monitoring aplikasi apapun yang memiliki koneksi jaringan. Berikut panduan lengkap untuk berbagai skenario monitoring.

## 🔍 Langkah 1: Temukan Nama Proses Aplikasi

### Menggunakan Script Finder
```bash
# Cari aplikasi umum yang sedang berjalan
python3 find_app_processes.py --common

# Cari aplikasi berdasarkan nama
python3 find_app_processes.py --name discord
python3 find_app_processes.py --name chrome
python3 find_app_processes.py --name spotify

# Cari aplikasi berdasarkan port
python3 find_app_processes.py --port 443
python3 find_app_processes.py --port 80

# Lihat semua koneksi jaringan
python3 find_app_processes.py --all
```

### Menggunakan Command Line
```bash
# Cek proses yang berjalan
ps aux | grep -i "nama_aplikasi"

# Cek dengan netstat
netstat -tulpn | grep "nama_aplikasi"

# Cek dengan lsof
lsof -i -P | grep "nama_aplikasi"

# Cek dengan ss
ss -tulpn | grep "nama_aplikasi"
```

## 🎮 Gaming Applications

### Steam
```bash
# Cari proses Steam
python3 find_app_processes.py --name steam

# Monitor Steam
python3 main.py --app-monitor steam --app-duration 300
python3 custom_app_monitor.py steam --session 300
```

### Discord
```bash
# Cari proses Discord
python3 find_app_processes.py --name discord

# Monitor Discord
python3 main.py --app-monitor discord --app-duration 300
python3 discord_monitor.py --continuous
python3 custom_app_monitor.py discord --session 300
```

### Epic Games
```bash
# Cari proses Epic Games
python3 find_app_processes.py --name epic

# Monitor Epic Games
python3 main.py --app-monitor epic --app-duration 300
python3 custom_app_monitor.py epic --session 300
```

### Battle.net
```bash
# Cari proses Battle.net
python3 find_app_processes.py --name battle

# Monitor Battle.net
python3 main.py --app-monitor battle --app-duration 300
python3 custom_app_monitor.py battle --session 300
```

## 🌐 Web Browsers

### Google Chrome
```bash
# Cari proses Chrome
python3 find_app_processes.py --name chrome

# Monitor Chrome
python3 main.py --app-monitor chrome --app-duration 300
python3 custom_app_monitor.py chrome --session 300
```

### Mozilla Firefox
```bash
# Cari proses Firefox
python3 find_app_processes.py --name firefox

# Monitor Firefox
python3 main.py --app-monitor firefox --app-duration 300
python3 custom_app_monitor.py firefox --session 300
```

### Microsoft Edge
```bash
# Cari proses Edge
python3 find_app_processes.py --name edge

# Monitor Edge
python3 main.py --app-monitor edge --app-duration 300
python3 custom_app_monitor.py edge --session 300
```

## 🎵 Media Applications

### Spotify
```bash
# Cari proses Spotify
python3 find_app_processes.py --name spotify

# Monitor Spotify
python3 main.py --app-monitor spotify --app-duration 300
python3 custom_app_monitor.py spotify --session 300
```

### VLC Media Player
```bash
# Cari proses VLC
python3 find_app_processes.py --name vlc

# Monitor VLC
python3 main.py --app-monitor vlc --app-duration 300
python3 custom_app_monitor.py vlc --session 300
```

## 💻 Development Tools

### Visual Studio Code
```bash
# Cari proses VS Code
python3 find_app_processes.py --name code

# Monitor VS Code
python3 main.py --app-monitor code --app-duration 300
python3 custom_app_monitor.py code --session 300
```

### Docker
```bash
# Cari proses Docker
python3 find_app_processes.py --name docker

# Monitor Docker
python3 main.py --app-monitor docker --app-duration 300
python3 custom_app_monitor.py docker --session 300
```

### Node.js
```bash
# Cari proses Node.js
python3 find_app_processes.py --name node

# Monitor Node.js
python3 main.py --app-monitor node --app-duration 300
python3 custom_app_monitor.py node --session 300
```

## 📧 Communication Apps

### Telegram
```bash
# Cari proses Telegram
python3 find_app_processes.py --name telegram

# Monitor Telegram
python3 main.py --app-monitor telegram --app-duration 300
python3 custom_app_monitor.py telegram --session 300
```

### WhatsApp Desktop
```bash
# Cari proses WhatsApp
python3 find_app_processes.py --name whatsapp

# Monitor WhatsApp
python3 main.py --app-monitor whatsapp --app-duration 300
python3 custom_app_monitor.py whatsapp --session 300
```

### Slack
```bash
# Cari proses Slack
python3 find_app_processes.py --name slack

# Monitor Slack
python3 main.py --app-monitor slack --app-duration 300
python3 custom_app_monitor.py slack --session 300
```

## 🔧 Advanced Monitoring Techniques

### 1. Monitor Multiple Applications
```bash
# Terminal 1: Monitor Discord
python3 custom_app_monitor.py discord --continuous &

# Terminal 2: Monitor Chrome
python3 custom_app_monitor.py chrome --continuous &

# Terminal 3: Monitor Spotify
python3 custom_app_monitor.py spotify --continuous &
```

### 2. Monitor by Port
```bash
# Cari aplikasi yang menggunakan port 443 (HTTPS)
python3 find_app_processes.py --port 443

# Cari aplikasi yang menggunakan port 80 (HTTP)
python3 find_app_processes.py --port 80

# Cari aplikasi yang menggunakan port 22 (SSH)
python3 find_app_processes.py --port 22
```

### 3. Monitor by Network Activity
```bash
# Lihat semua aplikasi dengan koneksi jaringan
python3 find_app_processes.py --network

# Lihat semua koneksi jaringan aktif
python3 find_app_processes.py --all
```

## 📊 Monitoring Output Examples

### Firefox Monitoring
```
🎯 Monitoring FIREFOX
==================================================
✅ firefox ditemukan! (1 processes)
📋 Process names: firefox-esr
   PID 7987: firefox-esr

⏱️  [ 45s/300s] Connections:   5 | Destinations:   5

📊 FIREFOX MONITORING COMPLETED
==================================================
⏱️  Duration: 300 seconds
🔗 Total Connections: 5
🌍 Unique Destinations: 5

📍 DESTINATIONS DISCOVERED:
   • 104.18.35.23 (Canada)
     Ports: 443
     Connections: 1
     Processes: firefox-esr

   • 34.107.243.93 (United States)
     Ports: 443
     Connections: 1
     Processes: firefox-esr

💾 Results saved to: logs/firefox_monitoring_1694000000.json
```

### Discord Monitoring
```
🎯 Monitoring DISCORD
==================================================
✅ discord ditemukan! (2 processes)
📋 Process names: Discord, Discord.exe
   PID 1234: Discord
   PID 5678: Discord.exe

⏱️  [ 45s/300s] Connections:  12 | Destinations:   8

📊 DISCORD MONITORING COMPLETED
==================================================
⏱️  Duration: 300 seconds
🔗 Total Connections: 12
🌍 Unique Destinations: 8

📍 DESTINATIONS DISCOVERED:
   • 162.159.128.233 (United States)
     Ports: 443, 80
     Connections: 5
     Processes: Discord

   • 104.16.248.249 (United States)
     Ports: 443
     Connections: 3
     Processes: Discord

💾 Results saved to: logs/discord_monitoring_1694000000.json
```

## 🚨 Troubleshooting

### 1. Aplikasi Tidak Ditemukan
```bash
# Cek dengan nama yang berbeda
python3 find_app_processes.py --name "nama_aplikasi"

# Cek dengan nama lengkap
python3 find_app_processes.py --name "NamaAplikasi.exe"

# Cek dengan path
python3 find_app_processes.py --name "/path/to/app"
```

### 2. Tidak Ada Koneksi
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

## 📈 Data Analysis

### 1. Analisis File JSON
```python
import json
import pandas as pd

# Load monitoring results
with open('logs/firefox_monitoring_1694000000.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
destinations = data['destinations']
df_data = []

for ip, info in destinations.items():
    df_data.append({
        'ip': ip,
        'country': info['country'],
        'ports': ','.join(map(str, info['ports'])),
        'connections': info['connections'],
        'processes': ','.join(info['processes'])
    })

df = pd.DataFrame(df_data)
print(df.head())

# Export to CSV
df.to_csv('firefox_analysis.csv', index=False)
```

### 2. Real-time Analysis
```python
from src.monitor.process_monitor import ProcessMonitor
from src.utils.geo_utils import GeoLocationUtils

monitor = ProcessMonitor()
geo = GeoLocationUtils()

# Get app connections
processes = monitor.get_process_by_name('firefox')
connections = []

for proc in processes:
    proc_connections = monitor._get_process_connections(proc['pid'])
    connections.extend(proc_connections)

# Analyze destinations
destinations = {}
for conn in connections:
    if conn['remote_address']:
        dest_ip = conn['remote_address']
        if dest_ip not in destinations:
            destinations[dest_ip] = {
                'ip': dest_ip,
                'country': geo.get_country(dest_ip),
                'connections': 0
            }
        destinations[dest_ip]['connections'] += 1

# Display results
for ip, info in destinations.items():
    print(f"{ip} ({info['country']}) - {info['connections']} connections")
```

## 🎯 Best Practices

### 1. Monitoring Duration
```bash
# Untuk testing cepat
python3 custom_app_monitor.py "nama_aplikasi" --session 60

# Untuk monitoring normal
python3 custom_app_monitor.py "nama_aplikasi" --session 300

# Untuk monitoring panjang
python3 custom_app_monitor.py "nama_aplikasi" --session 3600
```

### 2. Continuous Monitoring
```bash
# Monitor secara kontinyu
python3 custom_app_monitor.py "nama_aplikasi" --continuous

# Monitor dengan interval custom
python3 custom_app_monitor.py "nama_aplikasi" --continuous --interval 5
```

### 3. Data Logging
```bash
# Monitor dengan logging
python3 custom_app_monitor.py "nama_aplikasi" --session 300 2>&1 | tee app_monitor.log

# Monitor dengan output ke file
python3 custom_app_monitor.py "nama_aplikasi" --session 300 > app_monitor.log 2>&1
```

## 🔍 Custom Monitoring Scripts

### 1. Monitor Specific Ports
```python
#!/usr/bin/env python3
import subprocess
import time

def monitor_port(port: int, duration: int = 300):
    """Monitor aplikasi yang menggunakan port tertentu"""
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Cari proses yang menggunakan port
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        
        if result.stdout:
            print(f"Port {port} is being used:")
            print(result.stdout)
        
        time.sleep(5)

# Usage
monitor_port(443, 300)  # Monitor port 443 for 5 minutes
```

### 2. Monitor by Process Name Pattern
```python
#!/usr/bin/env python3
import psutil
import re

def monitor_by_pattern(pattern: str):
    """Monitor aplikasi berdasarkan pattern nama"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            proc_info = proc.info
            if re.search(pattern, proc_info['name'], re.IGNORECASE):
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return processes

# Usage
chrome_processes = monitor_by_pattern('chrome')
firefox_processes = monitor_by_pattern('firefox')
```

## 📋 Summary

### Tools yang Tersedia:
1. **find_app_processes.py** - Temukan nama proses aplikasi
2. **custom_app_monitor.py** - Monitor aplikasi kustom
3. **discord_monitor.py** - Monitor Discord khusus
4. **main.py** - Monitor aplikasi dengan main script

### Command Examples:
```bash
# Temukan aplikasi
python3 find_app_processes.py --common
python3 find_app_processes.py --name discord

# Monitor aplikasi
python3 main.py --app-monitor discord --app-duration 300
python3 custom_app_monitor.py firefox --session 300
python3 custom_app_monitor.py chrome --continuous

# Cek status
python3 custom_app_monitor.py discord --status
```

---

**Dengan panduan ini, Anda dapat memonitor aplikasi apapun yang memiliki koneksi jaringan!** 🚀
