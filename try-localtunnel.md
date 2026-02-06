# LocalTunnel Setup (Alternative to ngrok)

## Why LocalTunnel?
- Free and open source
- Better reliability for GET requests
- No request method limitations
- Simple setup

## Setup Steps:
1. Install Node.js (already have)
2. Install localtunnel
3. Run tunnel

## Commands:
# Install localtunnel
npm install -g localtunnel

# Run tunnel
npx localtunnel --port 8080 --subdomain barangay-reserve

# Or use random subdomain
npx localtunnel --port 8080
