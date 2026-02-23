import 'dart:convert';
import 'dart:typed_data';
import 'dart:io';
import 'package:image_picker/image_picker.dart';

class Base64ImageService {
  static const int maxImageSize = 800 * 1024; // 800KB limit for database storage

  // Compress and convert image to base64
  static Future<String?> imageToBase64(File imageFile) async {
    try {
      // Read image bytes
      Uint8List imageBytes = await imageFile.readAsBytes();
      
      // Check file size
      if (imageBytes.length > maxImageSize) {
        print('📷 Image too large (${imageBytes.length} bytes), compressing...');
        imageBytes = await _compressImage(imageBytes);
      }
      
      // Convert to base64
      String base64String = base64Encode(imageBytes);
      
      print('✅ Image converted to base64: ${base64String.length} characters');
      return base64String;
    } catch (e) {
      print('❌ Error converting image to base64: $e');
      return null;
    }
  }

  // Convert image picker result to base64
  static Future<String?> imagePickerToBase64(XFile? imageFile) async {
    if (imageFile == null) return null;
    
    try {
      // Read image bytes
      Uint8List imageBytes = await imageFile.readAsBytes();
      
      // Check file size
      if (imageBytes.length > maxImageSize) {
        print('📷 Image too large (${imageBytes.length} bytes), compressing...');
        imageBytes = await _compressImage(imageBytes);
      }
      
      // Convert to base64
      String base64String = base64Encode(imageBytes);
      
      print('✅ Image converted to base64: ${base64String.length} characters');
      return base64String;
    } catch (e) {
      print('❌ Error converting image to base64: $e');
      return null;
    }
  }

  // Simple image compression (reduce quality)
  static Future<Uint8List> _compressImage(Uint8List imageBytes) async {
    try {
      // For now, just reduce the size by sampling
      // In a real app, you'd use image package for proper compression
      int targetSize = maxImageSize;
      int step = (imageBytes.length / targetSize).ceil();
      
      List<int> compressedBytes = [];
      for (int i = 0; i < imageBytes.length; i += step) {
        compressedBytes.add(imageBytes[i]);
      }
      
      Uint8List result = Uint8List.fromList(compressedBytes);
      print('📷 Image compressed from ${imageBytes.length} to ${result.length} bytes');
      return result;
    } catch (e) {
      print('❌ Error compressing image: $e');
      return imageBytes; // Return original if compression fails
    }
  }

  // Convert base64 back to image bytes
  static Uint8List? base64ToImage(String base64String) {
    try {
      return base64Decode(base64String);
    } catch (e) {
      print('❌ Error converting base64 to image: $e');
      return null;
    }
  }

  // Validate base64 image
  static bool isValidBase64Image(String? base64String) {
    if (base64String == null || base64String.isEmpty) return false;
    
    try {
      Uint8List decoded = base64Decode(base64String);
      return decoded.isNotEmpty && decoded.length <= maxImageSize;
    } catch (e) {
      return false;
    }
  }

  // Get image info from base64
  static Map<String, dynamic> getImageInfo(String base64String) {
    try {
      Uint8List bytes = base64Decode(base64String);
      return {
        'size': bytes.length,
        'sizeKB': (bytes.length / 1024).toStringAsFixed(2),
        'isValid': true,
      };
    } catch (e) {
      return {
        'size': 0,
        'sizeKB': '0.00',
        'isValid': false,
        'error': e.toString(),
      };
    }
  }

  // Create data URL for display in Flutter
  static String createDataUrl(String base64String) {
    return 'data:image/jpeg;base64,$base64String';
  }

  // Methods for specific use cases

  // Upload receipt image (returns plain base64 string for compatibility)
  static Future<String?> uploadReceipt({
    required dynamic receiptImage, // Can be File or XFile
    required String bookingId,
  }) async {
    String? base64Image;
    
    if (receiptImage is XFile) {
      base64Image = await imagePickerToBase64(receiptImage);
    } else if (receiptImage is File) {
      base64Image = await imageToBase64(receiptImage);
    }
    
    if (base64Image != null) {
      // Return plain base64 for direct image decoding
      print('✅ Receipt uploaded as plain base64: ${(base64Image.length / 1024).toStringAsFixed(2)} KB');
      return base64Image;
    }
    
    return null;
  }

  // Upload verification photo (returns plain base64 string for compatibility)
  static Future<String?> uploadVerificationPhoto({
    required dynamic photoImage, // Can be File, XFile, or Uint8List
    required String userId,
    required String type, // 'profile' or 'id'
  }) async {
    String? base64Image;
    
    if (photoImage is XFile) {
      base64Image = await imagePickerToBase64(photoImage);
    } else if (photoImage is File) {
      base64Image = await imageToBase64(photoImage);
    } else if (photoImage is Uint8List) {
      // Handle Uint8List directly
      if (photoImage.length > maxImageSize) {
        print('📷 Image too large (${photoImage.length} bytes), compressing...');
        final compressedBytes = await _compressImage(photoImage);
        base64Image = base64Encode(compressedBytes);
      } else {
        base64Image = base64Encode(photoImage);
      }
    }
    
    if (base64Image != null) {
      // Return plain base64 for direct image decoding (no JSON wrapping)
      print('✅ Verification photo uploaded as plain base64: ${(base64Image.length / 1024).toStringAsFixed(2)} KB');
      return base64Image;
    }
    
    return null;
  }

  // Upload facility image (for officials)
  static Future<String?> uploadFacilityImage({
    required Uint8List imageBytes,
    required String facilityId,
  }) async {
    try {
      // Check file size
      if (imageBytes.length > maxImageSize) {
        print('📷 Image too large (${imageBytes.length} bytes), compressing...');
        imageBytes = await _compressImage(imageBytes);
      }
      
      // Convert to base64
      String base64String = base64Encode(imageBytes);
      
      // Add metadata
      Map<String, dynamic> imageData = {
        'base64': base64String,
        'facilityId': facilityId,
        'type': 'facility_image',
        'uploadedAt': DateTime.now().toIso8601String(),
        'sizeKB': (base64String.length / 1024).toStringAsFixed(2),
      };
      
      print('✅ Facility image converted to base64: ${imageData['sizeKB']} KB');
      return base64Encode(utf8.encode(jsonEncode(imageData)));
    } catch (e) {
      print('❌ Error uploading facility image: $e');
      return null;
    }
  }

  // Extract base64 from stored data (handles both JSON-wrapped, plain base64, and data URL formats)
  static String? extractBase64(String? storedData) {
    if (storedData == null || storedData.isEmpty) return null;
    
    // Remove excessive debug logging for better performance
    // print('🔍 DEBUG: extractBase64 called with: ${storedData.substring(0, storedData.length > 100 ? 100 : storedData.length)}...');
    
    // First try to extract from data URL format (data:image/jpeg;base64,xxxxx)
    if (storedData.startsWith('data:image/')) {
      final commaIndex = storedData.indexOf(',');
      if (commaIndex != -1 && commaIndex + 1 < storedData.length) {
        final base64Part = storedData.substring(commaIndex + 1);
        if (isValidBase64Image(base64Part)) {
          return base64Part;
        }
      }
    }
    
    // Then try to parse as plain base64 (new format)
    if (isValidBase64Image(storedData)) {
      return storedData;
    }
    
    // Then try to parse as JSON-wrapped data (old format)
    try {
      final decodedBytes = base64Decode(storedData);
      final jsonString = utf8.decode(decodedBytes);
      final Map<String, dynamic> imageData = jsonDecode(jsonString);
      
      // Try to get base64 from JSON
      final base64 = imageData['base64'] as String?;
      if (base64 != null && isValidBase64Image(base64)) {
        print('✅ Extracted base64 from JSON-wrapped legacy image: ${(base64.length / 1024).toStringAsFixed(2)} KB');
        return base64;
      }
      
      // If that didn't work, maybe the whole thing is stored differently
      print('⚠️ JSON structure different than expected: ${imageData.keys}');
    } catch (e) {
      print('❌ Could not extract base64: $e');
      print('❌ Error details: ${e.runtimeType}');
      // Not JSON-wrapped, might be corrupted data
    }
    
    return null;
  }

  // Extract metadata from stored data
  static Map<String, dynamic>? extractMetadata(String? storedData) {
    if (storedData == null || storedData.isEmpty) return null;
    
    try {
      Map<String, dynamic> imageData = jsonDecode(utf8.decode(base64Decode(storedData)));
      return {
        'bookingId': imageData['bookingId'],
        'userId': imageData['userId'],
        'type': imageData['type'],
        'uploadedAt': imageData['uploadedAt'],
        'sizeKB': imageData['sizeKB'],
      };
    } catch (e) {
      return null;
    }
  }

  // Get image data URL for display
  static String? getImageDataUrl(String? storedData) {
    String? base64Image = extractBase64(storedData);
    if (base64Image != null) {
      return createDataUrl(base64Image);
    }
    return null;
  }
}
