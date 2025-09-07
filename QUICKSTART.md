# 🚀 Quick Start Guide - Network Monitor

## Instalasi Cepat

```bash
# 1. Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip tcpdump libpcap-dev

# 2. Install Python packages
pip3 install -r requirements.txt

# 3. Jalankan aplikasi
sudo python3 main.py --dashboard
```

## Akses Dashboard

Buka browser dan kunjungi: **http://localhost:5000**

## Fitur Utama

### 📊 Dashboard Web
- Real-time monitoring
- Statistik koneksi
- Grafik traffic
- Daftar domain populer
- Alert system

### 🔍 Monitoring
- Capture paket jaringan
- Analisis destinasi akses
- Geolocation tracking
- Deteksi koneksi mencurigakan

### 💾 Database
- SQLite database
- Log koneksi lengkap
- Statistik historis
- Export data

## Command Line Options

```bash
# Dashboard web
python3 main.py --dashboard

# Monitoring saja
python3 main.py --monitor-only

# Tampilkan statistik
python3 main.py --stats

# Custom interface
python3 main.py --interface wlan0

# Custom port
python3 main.py --dashboard --port 8080
```

## Demo

```bash
# Jalankan demo
sudo python3 demo.py

# Test aplikasi
python3 test_monitor.py
```

## Troubleshooting

### Permission Error
```bash
sudo python3 main.py --dashboard
```

### Interface Error
```bash
# Cek interface tersedia
ip link show

# Gunakan interface yang benar
python3 main.py --interface wlan0
```

### Dependencies Error
```bash
pip3 install -r requirements.txt
```

## Systemd Service

```bash
# Install service
sudo ./install.sh

# Start service
sudo systemctl start network-monitor

# Enable auto-start
sudo systemctl enable network-monitor
```

## 📁 File Penting

- `main.py` - Entry point aplikasi
- `config/config.py` - Konfigurasi
- `src/dashboard/app.py` - Web dashboard
- `logs/network_monitor.db` - Database
- `logs/monitor.log` - Log aplikasi

## 🆘 Bantuan

1. Baca `README.md` untuk dokumentasi lengkap
2. Jalankan `python3 main.py --help` untuk opsi command
3. Cek log di `logs/monitor.log`
4. Test dengan `python3 test_monitor.py`

---

**Selamat menggunakan Network Monitor!** 🎉
