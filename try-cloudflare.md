# Cloudflare Tunnel Setup (Alternative to ngrok)

## Why Cloudflare Tunnel?
- Free for personal use
- Better reliability for GET requests
- More stable connections
- No request method limitations

## Setup Steps:
1. Install cloudflared
2. Create Cloudflare account (free)
3. Create tunnel
4. Configure to forward to localhost:8080

## Commands:
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe

# Authenticate
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create barangay-reserve

# Configure tunnel
cloudflared tunnel route dns barangay-reserve http://localhost:8080

# Run tunnel
cloudflared tunnel run barangay-reserve
