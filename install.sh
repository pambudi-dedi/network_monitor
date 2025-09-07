#!/bin/bash

# Network Monitor Installation Script

echo "=========================================="
echo "Network Monitor Installation Script"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update package list
echo "Updating package list..."
apt update

# Install Python dependencies
echo "Installing Python dependencies..."
apt install -y python3 python3-pip python3-venv

# Install system dependencies for scapy
echo "Installing system dependencies..."
apt install -y tcpdump libpcap-dev

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Make main script executable
chmod +x main.py

# Create systemd service file
echo "Creating systemd service..."
cat > /etc/systemd/system/network-monitor.service << EOF
[Unit]
Description=Network Monitor Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python $(pwd)/main.py --dashboard --host 0.0.0.0 --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

echo "=========================================="
echo "Installation completed!"
echo "=========================================="
echo ""
echo "To start the service:"
echo "  sudo systemctl start network-monitor"
echo ""
echo "To enable auto-start:"
echo "  sudo systemctl enable network-monitor"
echo ""
echo "To run manually:"
echo "  source venv/bin/activate"
echo "  python main.py --help"
echo ""
echo "Web dashboard will be available at:"
echo "  http://localhost:5000"
echo "=========================================="
