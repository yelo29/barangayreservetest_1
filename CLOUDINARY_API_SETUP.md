# CLOUDINARY API SETUP GUIDE

## 🌤️ Current Configuration

Your Cloudinary service is now configured with your API key:

- **Cloud Name**: `dxfqzoc8m`
- **API Key**: `381763147845335`
- **Upload Preset**: `barangay_reserve`

## 🔧 What's Been Implemented

### 1. **Enhanced Cloudinary Service**
- ✅ API key integration for better error handling
- ✅ Secure configuration with constants
- ✅ Enhanced logging and debugging
- ✅ Support for both public and private operations

### 2. **Upload Functionality**
- ✅ Receipt uploads for bookings
- ✅ Verification photo uploads
- ✅ Profile photo uploads
- ✅ Temporary file handling

### 3. **Advanced Features (Requires API Secret)**
- ⚠️ Image deletion (needs API secret)
- ⚠️ Image info retrieval (needs API secret)
- ⚠️ Advanced transformations (needs API secret)

## 🚨 Next Steps: Add API Secret

To enable full Cloudinary functionality:

1. **Get your API Secret** from Cloudinary Dashboard:
   - Go to https://cloudinary.com/console
   - Navigate to Settings → API Keys
   - Find your API Secret

2. **Update the service**:
   ```dart
   // In lib/services/cloudinary_service.dart
   static const String _apiSecret = 'your_actual_api_secret_here';
   ```

3. **For production security**, consider using environment variables:
   ```dart
   static const String _apiSecret = String.fromEnvironment('CLOUDINARY_API_SECRET');
   ```

## 🔍 Upload Preset Configuration

Make sure you have an upload preset named `barangay_reserve` in Cloudinary:

1. Go to Cloudinary Dashboard → Settings → Upload
2. Create upload preset with:
   - **Name**: `barangay_reserve`
   - **Signing Mode**: Unsigned
   - **Allowed Formats**: jpg, jpeg, png
   - **Folder**: `barangay_reserve`
   - **Unique Filename**: Enabled

## 📱 Testing the Integration

### Test Receipt Upload:
1. Login as resident
2. Try to create a booking
3. Upload a receipt image
4. Check logs for: `🌤️ Cloudinary - Upload successful`

### Test Verification Upload:
1. Go to verification screen
2. Upload profile photo and ID
3. Submit verification
4. Check logs for successful uploads

## 🐛 Troubleshooting

### Common Issues:
1. **"Upload preset not found"**
   - Create the upload preset in Cloudinary console
   - Make sure it's named exactly `barangay_reserve`

2. **"API key invalid"**
   - Verify the API key: `381763147845335`
   - Check if Cloudinary account is active

3. **"Network error"**
   - Check internet connection
   - Verify Cloudinary service is operational

### Debug Logs:
Look for these log messages:
- `🌤️ Cloudinary initialized successfully`
- `🌤️ Using API Key: 381763147845335`
- `🌤️ Cloudinary - Upload successful`

## 🔐 Security Notes

- ✅ API key is hardcoded (acceptable for demo)
- ⚠️ API secret should be in environment variables
- ✅ Upload preset is unsigned (safe for public uploads)
- ✅ Folder structure is organized

## 🚀 Production Deployment

For production deployment:

1. **Add API secret** to environment variables
2. **Enable signed uploads** for better security
3. **Set up CDN caching** for better performance
4. **Configure transformations** for image optimization

**Your Cloudinary integration is now properly configured with the API key!** 🎉
