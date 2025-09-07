# 📖 Usage Examples - Network Monitor

## 🎯 Monitoring Aplikasi Spesifik

### 1. Monitoring Discord

```bash
# Monitor Discord untuk 5 menit
python3 main.py --app-monitor discord --app-duration 300

# Monitor Discord untuk 10 menit
python3 main.py --app-monitor discord --app-duration 600

# Menggunakan Discord Monitor khusus
python3 discord_monitor.py --continuous
python3 discord_monitor.py --session 300
python3 discord_monitor.py --status
```

**Output Example:**
```
🎯 Monitoring DISCORD Network Activity
==================================================
✅ discord ditemukan! (2 processes)
   PID 1234: Discord
   PID 5678: Discord Helper

⏱️  [ 45s/300s] Connections:  12 | Destinations:   8

📊 DISCORD MONITORING COMPLETED
==================================================
⏱️  Duration: 300 seconds
🔗 Total Connections: 45
🌍 Unique Destinations: 12

📍 DESTINATIONS DISCOVERED:
   • 162.159.128.233
     Ports: 443, 80
     Connections: 15
     Processes: Discord

💾 Results saved to: logs/discord_monitoring_1694000000.json
```

### 2. Monitoring Browser (Chrome/Firefox)

```bash
# Monitor Chrome
python3 main.py --app-monitor chrome --app-duration 300

# Monitor Firefox
python3 main.py --app-monitor firefox --app-duration 300
```

### 3. Monitoring Gaming Applications

```bash
# Monitor Steam
python3 main.py --app-monitor steam --app-duration 600

# Monitor Epic Games
python3 main.py --app-monitor epic --app-duration 300
```

## 🌐 General Network Monitoring

### 1. Dashboard Web

```bash
# Jalankan dashboard web
python3 main.py --dashboard

# Dashboard dengan custom port
python3 main.py --dashboard --port 8080

# Dashboard dengan custom host
python3 main.py --dashboard --host 192.168.1.100 --port 5000
```

**Access:** `http://localhost:5000`

### 2. Monitoring Saja (Tanpa Dashboard)

```bash
# Monitor interface default (eth0)
python3 main.py --monitor-only

# Monitor interface tertentu
python3 main.py --monitor-only --interface wlan0

# Monitor dengan interface custom
python3 main.py --monitor-only --interface enp0s3
```

### 3. Menampilkan Statistik

```bash
# Tampilkan statistik dan keluar
python3 main.py --stats
```

**Output Example:**
```
==================================================
NETWORK MONITOR STATISTICS
==================================================
Monitoring Status: Running
Interface: eth0
Local IP: 192.168.1.100
Total Connections (24h): 1250
Unique Domains (24h): 45
Data Transferred (24h): 125.5 MB
Suspicious Connections (24h): 3
==================================================

TOP 5 DOMAINS:
1. discord.com - 45 accesses
2. google.com - 32 accesses
3. github.com - 28 accesses
4. stackoverflow.com - 15 accesses
5. youtube.com - 12 accesses

RECENT ALERTS:
- [WARNING] HIGH_TRAFFIC: High traffic detected: 150 connections in last minute
- [CRITICAL] SUSPICIOUS_CONNECTION: Suspicious connection: 192.168.1.100 -> 1.2.3.4:22
```

## 🔧 Advanced Usage

### 1. Monitoring Multiple Applications

```bash
# Terminal 1: Monitor Discord
python3 main.py --app-monitor discord --app-duration 600 &

# Terminal 2: Monitor Chrome
python3 main.py --app-monitor chrome --app-duration 600 &

# Terminal 3: Monitor Firefox
python3 main.py --app-monitor firefox --app-duration 600 &
```

### 2. Custom Monitoring Script

```python
#!/usr/bin/env python3
from src.monitor.process_monitor import ProcessMonitor
import time

monitor = ProcessMonitor()

# Monitor aplikasi custom
def monitor_app(app_name, duration):
    print(f"Monitoring {app_name} for {duration} seconds...")
    
    start_time = time.time()
    destinations = {}
    
    while time.time() - start_time < duration:
        processes = monitor.get_process_by_name(app_name)
        connections = []
        
        for proc in processes:
            proc_connections = monitor._get_process_connections(proc['pid'])
            connections.extend(proc_connections)
        
        # Process connections
        for conn in connections:
            if conn['remote_address']:
                dest_ip = conn['remote_address']
                if dest_ip not in destinations:
                    destinations[dest_ip] = 0
                destinations[dest_ip] += 1
        
        print(f"Connections: {len(connections)}, Destinations: {len(destinations)}")
        time.sleep(5)
    
    return destinations

# Usage
results = monitor_app('discord', 300)
print(f"Found {len(results)} unique destinations")
```

### 3. Systemd Service

```bash
# Install service
sudo ./install.sh

# Start service
sudo systemctl start network-monitor

# Check status
sudo systemctl status network-monitor

# View logs
sudo journalctl -u network-monitor -f

# Stop service
sudo systemctl stop network-monitor
```

## 📊 Data Analysis

### 1. Analisis File JSON

```python
import json
import pandas as pd

# Load monitoring results
with open('logs/discord_monitoring_1694000000.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
destinations = data['destinations']
df_data = []

for ip, info in destinations.items():
    df_data.append({
        'ip': ip,
        'ports': ','.join(map(str, info['ports'])),
        'connections': info['connections'],
        'processes': ','.join(info['processes'])
    })

df = pd.DataFrame(df_data)
print(df.head())

# Export to CSV
df.to_csv('discord_analysis.csv', index=False)
```

### 2. Real-time Analysis

```python
from src.monitor.process_monitor import ProcessMonitor
from src.utils.geo_utils import GeoLocationUtils

monitor = ProcessMonitor()
geo = GeoLocationUtils()

# Get Discord destinations
discord_connections = monitor.get_discord_connections()
destinations = {}

for conn in discord_connections:
    dest_ip = conn['remote_address']
    if dest_ip:
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

## 🚨 Troubleshooting

### 1. Permission Issues

```bash
# Jalankan dengan sudo
sudo python3 main.py --app-monitor discord --app-duration 300

# Atau gunakan systemd service
sudo systemctl start network-monitor
```

### 2. Application Not Found

```bash
# Cek proses yang berjalan
ps aux | grep discord

# Cek dengan nama yang berbeda
python3 main.py --app-monitor "Discord.exe" --app-duration 300

# Test dengan script test
python3 test_app_monitor.py
```

### 3. No Connections Found

```bash
# Pastikan aplikasi sedang aktif
# Buka Discord dan mulai voice call atau chat

# Cek firewall
sudo ufw status

# Test dengan aplikasi lain
python3 main.py --app-monitor chrome --app-duration 60
```

### 4. Interface Issues

```bash
# Cek interface yang tersedia
ip link show

# Cek interface yang aktif
ip addr show

# Gunakan interface yang benar
python3 main.py --monitor-only --interface wlan0
```

## 📈 Performance Tips

### 1. Optimize Monitoring Duration

```bash
# Untuk testing cepat
python3 main.py --app-monitor discord --app-duration 60

# Untuk monitoring panjang
python3 main.py --app-monitor discord --app-duration 3600  # 1 hour
```

### 2. Monitor Specific Processes

```bash
# Monitor hanya proses utama
python3 main.py --app-monitor discord --app-duration 300

# Hindari monitoring semua proses sistem
```

### 3. Use Logging

```bash
# Monitor dengan logging
python3 main.py --app-monitor discord --app-duration 300 2>&1 | tee discord_monitor.log
```

## 🔍 Debugging

### 1. Verbose Output

```bash
# Test dengan verbose output
python3 test_app_monitor.py

# Test Discord monitor
python3 discord_monitor.py --status
```

### 2. Check Logs

```bash
# Application logs
tail -f logs/monitor.log

# Discord monitor logs
tail -f logs/discord_monitor.log

# System logs
sudo journalctl -u network-monitor -f
```

### 3. Database Inspection

```bash
# Check database
sqlite3 logs/network_monitor.db "SELECT COUNT(*) FROM network_connections;"

# Check recent connections
sqlite3 logs/network_monitor.db "SELECT * FROM network_connections ORDER BY timestamp DESC LIMIT 10;"
```

---

**Network Monitor** memberikan fleksibilitas penuh untuk monitoring aplikasi dan network traffic! 🚀
