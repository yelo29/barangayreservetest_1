# Ngrok Setup Instructions

## 1. Create New Account
1. Go to: https://dashboard.ngrok.com/signup
2. Fill in your details (use different email than leo052904@gmail.com)
3. Verify your email address
4. Choose the free plan

## 2. Get Your Authtoken
1. After signing up, go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy your authtoken (it will look like: `2abcdef1234567890abcdef1234567890`)
3. Keep it safe - you'll need it for the next step

## 3. Configure Ngrok
Once you have your authtoken, run:
```
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

## 4. Start Ngrok
```
ngrok http 8080
```

## 5. Update Flutter Config
Update `lib/config/app_config.dart` with your new ngrok URL.
