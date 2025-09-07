# Network Monitor

Aplikasi monitoring network traffic yang memungkinkan Anda untuk melacak destinasi akses jaringan secara real-time. Aplikasi ini menggunakan Python dengan library Scapy untuk menangkap dan menganalisis paket jaringan.

## 🚀 Fitur Utama

- **Real-time Network Monitoring**: Monitor traffic jaringan secara real-time
- **Web Dashboard**: Interface web yang modern dan responsif untuk visualisasi data
- **Database Logging**: Menyimpan log koneksi ke database SQLite
- **Geolocation**: Menampilkan informasi negara dari IP address
- **Alert System**: Sistem peringatan untuk koneksi mencurigakan
- **Statistics**: Statistik lengkap tentang koneksi dan traffic
- **Top Domains**: Daftar domain yang paling sering diakses
- **Suspicious Detection**: Deteksi koneksi mencurigakan berdasarkan port dan domain

## 📋 Persyaratan Sistem

- **OS**: Linux (Ubuntu/Debian recommended)
- **Python**: 3.8 atau lebih baru
- **Root Access**: Diperlukan untuk menangkap paket jaringan
- **Network Interface**: Interface jaringan yang aktif

## 🛠️ Instalasi

### Metode 1: Instalasi Otomatis (Recommended)

```bash
# Clone atau download proyek
cd network_monitor

# Jalankan script instalasi
sudo ./install.sh
```

### Metode 2: Instalasi Manual

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install -y python3 python3-pip tcpdump libpcap-dev

# Install Python packages
pip3 install -r requirements.txt

# Buat direktori logs
mkdir -p logs
```

## 🚀 Cara Penggunaan

### 1. Menjalankan Dashboard Web

```bash
# Menjalankan dengan dashboard web
python3 main.py --dashboard

# Atau dengan custom host dan port
python3 main.py --dashboard --host 0.0.0.0 --port 8080
```

Dashboard akan tersedia di: `http://localhost:5000`

### 2. Monitoring Saja (Tanpa Dashboard)

```bash
# Menjalankan monitoring saja
python3 main.py --monitor-only --interface eth0
```

### 3. Menampilkan Statistik

```bash
# Menampilkan statistik dan keluar
python3 main.py --stats
```

### 4. Menggunakan Systemd Service

```bash
# Start service
sudo systemctl start network-monitor

# Enable auto-start
sudo systemctl enable network-monitor

# Check status
sudo systemctl status network-monitor

# View logs
sudo journalctl -u network-monitor -f
```

## 📊 Dashboard Web

Dashboard web menyediakan:

- **Real-time Statistics**: Total koneksi, domain unik, data transfer, koneksi mencurigakan
- **Connection Chart**: Grafik koneksi per jam dalam 24 jam terakhir
- **Recent Connections**: Tabel koneksi terbaru dengan detail lengkap
- **Top Domains**: Daftar domain yang paling sering diakses
- **Alerts**: Daftar peringatan dan koneksi mencurigakan
- **Control Panel**: Tombol start/stop monitoring

## 🔧 Konfigurasi

File konfigurasi utama: `config/config.py`

```python
# Monitoring configuration
MONITORING_CONFIG = {
    "interface": "eth0",        # Network interface
    "capture_timeout": 1,       # Timeout dalam detik
    "max_packets": 1000,        # Maksimal paket per capture
    "log_interval": 60,         # Interval log dalam detik
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
}

# Alert thresholds
ALERT_THRESHOLDS = {
    "max_connections_per_minute": 100,
    "suspicious_domains": [
        "malware.com",
        "phishing.com",
        "suspicious.com"
    ]
}
```

## 📁 Struktur Proyek

```
network_monitor/
├── src/
│   ├── monitor/
│   │   └── network_monitor.py    # Modul monitoring utama
│   ├── database/
│   │   └── db_manager.py         # Database manager
│   ├── dashboard/
│   │   ├── app.py               # Flask web app
│   │   └── templates/
│   │       └── dashboard.html   # Dashboard template
│   └── utils/
│       └── geo_utils.py         # Geolocation utilities
├── config/
│   └── config.py               # Konfigurasi aplikasi
├── logs/                       # Direktori log dan database
├── main.py                     # Entry point aplikasi
├── requirements.txt            # Python dependencies
├── setup.py                    # Setup script
├── install.sh                  # Installation script
└── README.md                   # Dokumentasi
```

## 🔍 Fitur Monitoring

### Deteksi Koneksi Mencurigakan

Aplikasi mendeteksi koneksi mencurigakan berdasarkan:

- **Port Mencurigakan**: SSH (22), Telnet (23), RDP (3389), dll.
- **Domain Mencurigakan**: Domain yang terdaftar dalam blacklist
- **Traffic Tinggi**: Koneksi berlebihan dalam waktu singkat

### Informasi yang Dicatat

- Source IP dan Destination IP
- Port dan Protocol (TCP/UDP)
- Domain name (jika tersedia)
- Ukuran paket
- Negara tujuan (geolocation)
- Timestamp
- Status mencurigakan

## 🚨 Alert System

Sistem alert akan mengirimkan notifikasi untuk:

- Koneksi ke domain mencurigakan
- Traffic berlebihan (>100 koneksi/menit)
- Koneksi ke port yang mencurigakan
- Aktivitas anomali lainnya

## 📈 Database Schema

### Tabel `network_connections`
- `id`: Primary key
- `timestamp`: Waktu koneksi
- `source_ip`: IP sumber
- `dest_ip`: IP tujuan
- `dest_port`: Port tujuan
- `protocol`: Protocol (TCP/UDP)
- `dest_domain`: Domain tujuan
- `packet_size`: Ukuran paket
- `country`: Negara tujuan
- `is_suspicious`: Status mencurigakan

### Tabel `alerts`
- `id`: Primary key
- `timestamp`: Waktu alert
- `alert_type`: Jenis alert
- `message`: Pesan alert
- `severity`: Tingkat keparahan
- `is_resolved`: Status resolved

## 🛡️ Keamanan

- **Root Access**: Diperlukan untuk menangkap paket jaringan
- **Network Interface**: Hanya monitor interface yang ditentukan
- **Data Privacy**: Data disimpan lokal, tidak dikirim ke server eksternal
- **Access Control**: Dashboard dapat dibatasi dengan firewall

## 🔧 Troubleshooting

### Error: "Permission denied"
```bash
# Pastikan menjalankan dengan root
sudo python3 main.py --dashboard
```

### Error: "No such device: eth0"
```bash
# Cek interface yang tersedia
ip link show

# Gunakan interface yang benar
python3 main.py --interface wlan0
```

### Error: "Module not found"
```bash
# Install dependencies
pip3 install -r requirements.txt
```

### Dashboard tidak bisa diakses
```bash
# Cek firewall
sudo ufw allow 5000

# Cek apakah service berjalan
sudo systemctl status network-monitor
```

## 📝 Log Files

- **Application Log**: `logs/monitor.log`
- **Database**: `logs/network_monitor.db`
- **System Log**: `journalctl -u network-monitor`

## 🤝 Kontribusi

1. Fork proyek
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

Jika mengalami masalah atau memiliki pertanyaan:

1. Cek bagian Troubleshooting
2. Lihat log files
3. Buat issue di repository
4. Hubungi tim development

## 🔄 Update

Untuk update aplikasi:

```bash
# Backup database
cp logs/network_monitor.db logs/network_monitor.db.backup

# Update code
git pull origin main

# Restart service
sudo systemctl restart network-monitor
```

---

**Network Monitor** - Monitor network traffic dengan mudah dan efisien! 🚀
