# 🚀 Barangay Reserve - Dynamic IP Deployment Guide

## 🌐 No More APK Rebuilds! Dynamic Server Configuration

This guide shows how to set up your server to work with any IP address using DuckDNS, so you'll never need to rebuild your APK again!

---

## 📋 What's New

### ✅ Dynamic Server Configuration
- **Server accepts all connections** (`host='0.0.0.0'`)
- **Flutter app can change server URL** without rebuilding
- **DuckDNS integration** for dynamic domains
- **Runtime server configuration** screen in the app

### ✅ Key Features
- 🎯 **No hardcoded IPs** in the Flutter app
- 🔄 **Runtime configuration** - change server URL anytime
- 🦆 **DuckDNS support** - use custom domain
- 🌐 **CORS flexibility** - works with any domain/IP
- 💾 **Persistent settings** - saves configuration locally

---

## 🔧 Server Setup

### 1. Copy Server Files
```bash
# Copy these 4 files to your server:
server/
├── server.py              # Main Flask app (updated)
├── config.py              # Dynamic configuration
├── barangay.db           # Your database
├── requirements.txt      # Dependencies (updated)
├── duckdns_updater.py   # DuckDNS automation
└── .env.example         # Environment template
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy the template
cp .env.example .env

# Edit the configuration
nano .env
```

**Example .env file:**
```env
# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG=False

# CORS Settings (allow all origins)
CORS_ORIGINS=*

# Database
DB_PATH=barangay.db

# DuckDNS (optional but recommended)
DUCKDNS_DOMAIN=mybarangay.duckdns.org
DUCKDNS_TOKEN=your-duckdns-token
```

### 4. Start the Server
```bash
python server.py
```

**Server will now accept connections from any IP address!**

---

## 🦆 DuckDNS Setup (Optional but Recommended)

### 1. Create DuckDNS Account
1. Go to [duckdns.org](https://duckdns.org)
2. Sign up with GitHub, Reddit, or email
3. Create a subdomain (e.g., `mybarangay.duckdns.org`)

### 2. Configure DuckDNS Updater
```bash
# Interactive setup
python duckdns_updater.py setup

# One-time update
python duckdns_updater.py update

# Auto-update mode (runs continuously)
python duckdns_updater.py auto
```

### 3. Test DuckDNS
```bash
# Check if your domain resolves
curl http://mybarangay.duckdns.org:8080/api/me?email=test@example.com
```

---

## 📱 Flutter App Configuration

### ✅ New Features in the App

#### 1. **Server Configuration Screen**
- **Runtime URL changes** - no rebuild needed
- **Connection testing** - verify server works
- **Quick setup buttons** - localhost, DuckDNS, HTTPS
- **URL validation** - prevents invalid inputs

#### 2. **Dynamic API Service**
- **No hardcoded URLs** - uses AppConfig
- **Automatic loading** - loads saved config on startup
- **Flexible CORS** - works with any domain

#### 3. **Main Screen Updates**
- **Server config button** - easy access
- **Current URL display** - see what's configured
- **Visual feedback** - connection status

---

## 🚀 Complete Deployment Steps

### Step 1: Server Setup
```bash
# 1. Copy files to server
# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Start server
python server.py
```

### Step 2: DuckDNS Setup (Optional)
```bash
# 1. Create DuckDNS account
# 2. Run setup
python duckdns_updater.py setup

# 3. Test update
python duckdns_updater.py update
```

### Step 3: Flutter App Setup
1. **Build APK once** - no hardcoded IPs
2. **Install on devices**
3. **Open app** - go to main screen
4. **Tap "Server Configuration"**
5. **Enter your server URL:**
   - `http://192.168.1.100:8080` (local IP)
   - `http://mybarangay.duckdns.org:8080` (DuckDNS)
   - `https://mybarangay.duckdns.org` (HTTPS)
6. **Test Connection** - verify it works
7. **Save Configuration** - persists across app restarts

---

## 🌐 Network Configuration Examples

### Local Network
```env
# For home/office network
CORS_ORIGINS=http://192.168.1.100:8080,http://localhost:8080
```

### DuckDNS Domain
```env
# For dynamic DNS
DUCKDNS_DOMAIN=mybarangay.duckdns.org
CORS_ORIGINS=*
```

### Production HTTPS
```env
# For production with SSL
DUCKDNS_DOMAIN=mybarangay.duckdns.org
CORS_ORIGINS=https://mybarangay.duckdns.org
```

---

## 🔍 Testing & Verification

### 1. Server Test
```bash
# Test server is running
curl http://localhost:8080/api/me?email=test@example.com
```

### 2. DuckDNS Test
```bash
# Test DuckDNS resolves
curl http://mybarangay.duckdns.org:8080/api/me?email=test@example.com
```

### 3. Flutter App Test
1. Open app
2. Check current server URL displayed
3. Tap "Server Configuration"
4. Enter your server URL
5. Tap "Test Connection"
6. Should show "Server connection successful!"

---

## 🚨 Troubleshooting

### Server Issues
```bash
# Check if server is running
netstat -tulpn | grep :8080

# Check logs
python server.py 2>&1 | tee server.log
```

### DuckDNS Issues
```bash
# Test IP detection
curl https://api.ipify.org

# Manual DuckDNS update
curl "https://duckdns.org/update?domains=DOMAIN&token=TOKEN&ip=$(curl -s https://api.ipify.org)"
```

### Flutter App Issues
1. **Check server URL format** - must include `http://` or `https://`
2. **Test connection** - use the test button
3. **Check CORS** - server must allow your domain
4. **Network permissions** - ensure device can reach server

---

## 🎯 Success Checklist

- [ ] **Server running** on `0.0.0.0:8080`
- [ ] **Dependencies installed** (`pip install -r requirements.txt`)
- [ ] **Environment configured** (`.env` file)
- [ ] **DuckDNS setup** (optional but recommended)
- [ ] **Flutter app built** (no hardcoded IPs)
- [ ] **Server URL configured** in app
- [ ] **Connection tested** successfully
- [ ] **Configuration saved** persists across restarts

---

## 🎉 Benefits

### ✅ What You Get
- **No more APK rebuilds** when IP changes
- **Dynamic server configuration** in the app
- **DuckDNS integration** for permanent domain
- **Flexible CORS** for any network setup
- **Runtime server changes** without code changes
- **Production-ready** configuration system

### 🚀 Perfect For
- **Home networks** with dynamic IPs
- **Multiple locations** with different networks
- **Testing environments** that change
- **Production deployments** with domains
- **Development setups** across devices

---

## 📞 Support

Your Barangay Reserve system is now **truly dynamic**! 

**No more rebuilding APKs for IP changes - just configure and go!** 🎓✨

The system will work with:
- ✅ **Local IPs** (192.168.x.x)
- ✅ **Public IPs** (dynamic or static)
- ✅ **DuckDNS domains** (mybarangay.duckdns.org)
- ✅ **Custom domains** (with SSL)
- ✅ **Any network setup** you can imagine!

🚀 **Deploy once, configure anywhere!**
