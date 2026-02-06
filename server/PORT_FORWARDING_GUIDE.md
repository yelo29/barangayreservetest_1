# 🌐 Port Forwarding Guide for Global Server Access

## 🎯 Goal: Make your server accessible from anywhere

## 📡 What You Need:
- Router admin access
- Your server running on 192.168.100.4:8080
- DuckDNS pointing to 110.93.84.131

## 🔧 Step-by-Step Port Forwarding:

### Step 1: Access Router Admin
1. Find your router's IP (usually 192.168.100.1 or 192.168.1.1)
2. Login to router admin panel
3. Look for "Port Forwarding" or "Virtual Server"

### Step 2: Configure Port Forwarding
- **External Port:** 8080
- **Internal Port:** 8080  
- **Internal IP:** 192.168.100.4 (your laptop)
- **Protocol:** TCP
- **Enable:** Yes

### Step 3: Test External Access
1. From different network, test: http://barangay-reserve.duckdns.org:8080
2. Should reach your server!

## 🌍 Result: True Global Server
- Works from any WiFi
- Works on mobile data
- Works from anywhere
- Perfect for school deployment

## ⚠️ Important Notes:
- Your laptop must be on and server running
- IP might change if you move networks
- Consider using a dedicated computer for server

## 🎯 Alternative: Use Public IP Directly
If port forwarding doesn't work, use: http://110.93.84.131:8080
