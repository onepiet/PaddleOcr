#!/bin/bash
# =========================================================================
# BIDSETU PaddleOCR Microservice — Hostinger VPS Installer Script
# =========================================================================

set -e

echo "========================================================================="
echo "BIDSETU — HOSTINGER VPS AUTOMATED INSTALLER"
echo "========================================================================="

# 1. Update package index and install curl & git
echo "[1/5] Updating system packages..."
sudo apt-get update -y
sudo apt-get install -y curl git ufw nginx

# 2. Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "[2/5] Installing Docker Engine..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
else
    echo "[2/5] Docker is already installed."
fi

# 3. Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "[3/5] Installing Docker Compose..."
    sudo apt-get install -y docker-compose-plugin docker-compose
fi

# 4. Build and Launch Container
echo "[4/5] Building and launching PaddleOCR container via Docker Compose..."
sudo docker-compose down || true
sudo docker-compose up --build -d

# 5. Configure Firewall & Nginx Reverse Proxy
echo "[5/5] Configuring Hostinger VPS Firewall & Nginx..."
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable || true

sudo cp nginx.conf /etc/nginx/sites-available/bidsetu-ocr
sudo ln -sf /etc/nginx/sites-available/bidsetu-ocr /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default || true
sudo nginx -t
sudo systemctl restart nginx

echo "========================================================================="
echo "DEPLOYMENT COMPLETE!"
echo "========================================================================="
echo "• Local Container API:  http://127.0.0.1:8000"
echo "• Health Endpoint:       http://localhost:8000/health"
echo "• Public VPS URL:        http://$(curl -s ifconfig.me)"
echo "• OCR Endpoint:          http://$(curl -s ifconfig.me)/ocr/process"
echo "========================================================================="
