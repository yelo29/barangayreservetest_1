# 🚀 Ngrok Quick Start - Instant Global Server

## 🎯 Get Global Access in 2 Minutes!

### Step 1: Download Ngrok
1. Go to: https://ngrok.com/download
2. Download Windows version
3. Extract the zip file
4. Run ngrok.exe

### Step 2: Start Your Server
```bash
# Make sure your server is running
cd server
python server.py
# Server running on: http://localhost:8080
```

### Step 3: Expose to Internet
```bash
# In ngrok terminal
ngrok http 8080
```

### Step 4: Get Your Global URL
Ngrok will show:
```
Forwarding                    https://abc123.ngrok.io -> http://localhost:8080
```

### Step 5: Update Your App
1. Open Barangay Reserve app
2. Server Configuration
3. Enter: https://abc123.ngrok.io
4. Test Connection → Should work!
5. Save Configuration

## 🌍 Result:
- Works from ANYWHERE in the world
- No router configuration needed
- HTTPS included (secure)
- Perfect for demos and testing

## 📱 Test from Different Networks:
- School WiFi ✅
- Home WiFi ✅
- Mobile data ✅
- Friend's phone ✅

## ⚠️ Important:
- Free ngrok URLs change each session
- For permanent URL, upgrade to paid plan
- Perfect for development and demos
