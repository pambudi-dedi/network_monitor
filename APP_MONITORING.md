# 🎯 Application-Specific Network Monitoring

Network Monitor mendukung monitoring destinasi akses untuk aplikasi spesifik seperti Discord, Chrome, Firefox, dan aplikasi lainnya.

## 🚀 Cara Menggunakan

### 1. Monitoring Discord

```bash
# Monitor Discord untuk 5 menit (300 detik)
python3 main.py --app-monitor discord --app-duration 300

# Monitor Discord untuk 10 menit
python3 main.py --app-monitor discord --app-duration 600
```

### 2. Monitoring Aplikasi Lain

```bash
# Monitor Chrome
python3 main.py --app-monitor chrome --app-duration 300

# Monitor Firefox
python3 main.py --app-monitor firefox --app-duration 300

# Monitor Steam
python3 main.py --app-monitor steam --app-duration 300

# Monitor Spotify
python3 main.py --app-monitor spotify --app-duration 300
```

### 3. Menggunakan Discord Monitor Khusus

```bash
# Monitor Discord secara kontinyu
python3 discord_monitor.py --continuous

# Monitor Discord untuk sesi tertentu
python3 discord_monitor.py --session 300

# Cek status Discord saat ini
python3 discord_monitor.py --status
```

## 📊 Output yang Dihasilkan

### Real-time Monitoring
```
🎯 Monitoring DISCORD Network Activity
==================================================
✅ discord ditemukan! (2 processes)
   PID 1234: Discord
   PID 5678: Discord Helper

⏱️  [ 45s/300s] Connections:  12 | Destinations:   8
```

### Hasil Akhir
```
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

   • 104.16.248.249
     Ports: 443
     Connections: 8
     Processes: Discord
```

## 📁 File Output

### 1. Log File
- **Location**: `logs/discord_monitor.log`
- **Content**: Real-time monitoring log

### 2. Session Data (JSON)
- **Location**: `logs/discord_session_YYYYMMDD_HHMMSS.json`
- **Content**: Data lengkap sesi monitoring

### 3. Monitoring Results
- **Location**: `logs/{app_name}_monitoring_{timestamp}.json`
- **Content**: Hasil monitoring aplikasi

## 🔍 Informasi yang Dicatat

### Untuk Setiap Koneksi:
- **Source IP & Port**: IP dan port lokal
- **Destination IP & Port**: IP dan port tujuan
- **Process Information**: Nama proses dan PID
- **Timestamp**: Waktu koneksi
- **Connection Status**: Status koneksi

### Untuk Setiap Destinasi:
- **IP Address**: Alamat IP tujuan
- **Ports Used**: Port yang digunakan
- **Connection Count**: Jumlah koneksi
- **Processes**: Proses yang menggunakan destinasi
- **First/Last Seen**: Waktu pertama dan terakhir terlihat

## 🎯 Aplikasi yang Didukung

### Gaming Applications
- **Discord**: Voice chat dan messaging
- **Steam**: Gaming platform
- **Epic Games**: Gaming launcher
- **Battle.net**: Blizzard games

### Web Browsers
- **Chrome**: Google Chrome browser
- **Firefox**: Mozilla Firefox browser
- **Safari**: Apple Safari browser
- **Edge**: Microsoft Edge browser

### Media Applications
- **Spotify**: Music streaming
- **Netflix**: Video streaming
- **YouTube**: Video platform
- **Twitch**: Live streaming

### Development Tools
- **VS Code**: Code editor
- **Git**: Version control
- **Docker**: Container platform
- **Node.js**: JavaScript runtime

## ⚙️ Konfigurasi Lanjutan

### Custom Process Names
Jika aplikasi memiliki nama proses yang tidak standar, Anda dapat memodifikasi `ProcessMonitor` class:

```python
# Di src/monitor/process_monitor.py
def get_custom_processes(self, custom_names: List[str]):
    processes = []
    for name in custom_names:
        processes.extend(self.get_process_by_name(name))
    return processes
```

### Filtering Options
```python
# Filter berdasarkan port
def filter_by_port(self, connections: List[Dict], ports: List[int]):
    return [conn for conn in connections if conn['remote_port'] in ports]

# Filter berdasarkan IP range
def filter_by_ip_range(self, connections: List[Dict], ip_range: str):
    # Implementasi filtering berdasarkan IP range
    pass
```

## 🚨 Troubleshooting

### Aplikasi Tidak Ditemukan
```bash
# Cek proses yang berjalan
ps aux | grep discord

# Cek dengan nama yang berbeda
python3 main.py --app-monitor "Discord.exe" --app-duration 300
```

### Permission Error
```bash
# Jalankan dengan sudo
sudo python3 main.py --app-monitor discord --app-duration 300
```

### Tidak Ada Koneksi
- Pastikan aplikasi sedang aktif digunakan
- Cek firewall settings
- Pastikan aplikasi memiliki koneksi internet

## 📈 Analisis Data

### Menggunakan Data JSON
```python
import json

# Load hasil monitoring
with open('logs/discord_monitoring_1234567890.json', 'r') as f:
    data = json.load(f)

# Analisis destinasi
destinations = data['destinations']
for ip, info in destinations.items():
    print(f"IP: {ip}")
    print(f"Ports: {info['ports']}")
    print(f"Connections: {info['connections']}")
```

### Export ke CSV
```python
import pandas as pd

# Convert ke DataFrame
df = pd.DataFrame([
    {
        'ip': ip,
        'ports': ','.join(map(str, info['ports'])),
        'connections': info['connections']
    }
    for ip, info in destinations.items()
])

# Export ke CSV
df.to_csv('discord_destinations.csv', index=False)
```

## 🔧 Advanced Usage

### Monitoring Multiple Apps
```bash
# Monitor Discord dan Chrome secara bersamaan
python3 main.py --app-monitor discord --app-duration 300 &
python3 main.py --app-monitor chrome --app-duration 300 &
```

### Custom Monitoring Script
```python
from src.monitor.process_monitor import ProcessMonitor

monitor = ProcessMonitor()

# Monitor aplikasi custom
def monitor_custom_app(app_name, duration):
    processes = monitor.get_process_by_name(app_name)
    # Custom monitoring logic
    pass
```

---

**Application-Specific Monitoring** memungkinkan Anda untuk memahami dengan detail kemana aplikasi mengakses data dan berkomunikasi! 🎯
