# Cloudinary Upload Preset Setup

## 🎯 Required Preset: "barangay_reserve"

### Steps to Create:

1. **Go to Cloudinary Console**
   - Login to https://cloudinary.com/console
   - Go to Settings → Upload

2. **Create New Upload Preset**
   - Click "Add upload preset"
   - **Name**: `barangay_reserve`
   - **Signing Mode**: `Unsigned` ⚠️ IMPORTANT
   - **Allowed Formats**: `jpg, jpeg, png`
   - **Folder**: Leave empty (will use folder from code)
   - **Unique Filename**: ✅ Enabled
   - **Overwrite**: ✅ Enabled

3. **Save the preset**

### ⚠️ Critical Settings:
- **Signing Mode MUST be Unsigned** - otherwise you'll get 401 errors
- **Name MUST be exactly "barangay_reserve"** - case sensitive

## 🔧 API Key Issue:

Your app is using API Key: `381763147845335`
But your environment shows: `524993157895526` (newest)

### Options:
1. **Keep using current key** (381763147845335) - just create the preset
2. **Update to new key** - change in cloudinary_service_new.dart

## 📱 After Setup:
1. Create the preset
2. Test image uploads
3. Should work without 401 errors
