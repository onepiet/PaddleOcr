# 🚀 BIDSETU PaddleOCR Microservice — Hostinger VPS Deployment Guide

This standalone folder (`bidsetu-ocr-vps`) is optimized for **Hostinger VPS** (Ubuntu 20.04/22.04/24.04 64-bit).

---

## 📋 Quick 1-Click Deployment on Hostinger VPS

### Step 1: Upload this Folder to Your Hostinger VPS
Connect to your Hostinger VPS via SSH or SFTP and copy the `bidsetu-ocr-vps` directory:
```bash
scp -r bidsetu-ocr-vps root@YOUR_HOSTINGER_VPS_IP:/root/
```

---

### Step 2: SSH into Your Hostinger VPS
```bash
ssh root@YOUR_HOSTINGER_VPS_IP
cd /root/bidsetu-ocr-vps
```

---

### Step 3: Run the 1-Click Deployment Script
Make the script executable and run it:
```bash
chmod +x deploy_vps.sh
./deploy_vps.sh
```

The script will automatically:
1. Install Docker, Docker Compose, and Nginx.
2. Build the high-accuracy PaddleOCR & PyMuPDF Docker container.
3. Open firewall ports `80`, `443`, and `8000`.
4. Configure Nginx reverse proxy for sub-second API requests.

---

## 🧪 Verification & Health Check

Test your live Hostinger VPS endpoint:
```bash
curl http://YOUR_HOSTINGER_VPS_IP/health
```

**Expected Output:**
```json
{
  "status": "ok",
  "ocr": "available",
  "engine": "PaddleOCR",
  "version": "v3.7.0",
  "device": "cpu"
}
```

---

## 🔒 Connect Next.js App to Hostinger VPS OCR Service

In your BIDSETU Next.js application `.env.local` file, set:
```env
OCR_SERVICE_URL=http://YOUR_HOSTINGER_VPS_IP
```

---

## 📄 SSL Certificate Setup (Domain Name - Optional)
If you point a domain (e.g. `ocr.bidsetu.org`) to your Hostinger VPS IP:
```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d ocr.bidsetu.org
```
Certbot will automatically install HTTPS SSL certificates!
