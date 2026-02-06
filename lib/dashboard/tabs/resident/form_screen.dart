import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import '../../../services/auth_api_service.dart';
import '../../../services/api_service.dart';
import '../../../services/base64_image_service.dart';
import '../../../models/facility_model.dart';
import '../../../config/app_config.dart';

class FormScreen extends StatefulWidget {
  final String facilityName;
  final String facilityId;
  final String selectedDate;
  final String facilityRate;
  final VoidCallback? onBookingSubmitted;

  const FormScreen({
    super.key,
    required this.facilityName,
    required this.facilityId,
    required this.selectedDate,
    required this.facilityRate,
    this.onBookingSubmitted,
  });

  @override
  State<FormScreen> createState() => _FormScreenState();
}

class _FormScreenState extends State<FormScreen> {
  final FirebaseService _firebaseService = FirebaseService();
  final ImagePicker _imagePicker = ImagePicker();

  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _contactController = TextEditingController();
  final _addressController = TextEditingController();
  final _purposeController = TextEditingController();
  final _gcashNumberController = TextEditingController();
  final _gcashNameController = TextEditingController();
  final _gcashEmailController = TextEditingController();
  final _receiptDetailsController = TextEditingController();

  String? _selectedTimeslot;
  File? _receiptImage;
  bool _isLoading = false;
  String? _errorMessage;

  final List<String> _timeslots = [
  '08:00-09:00',
  '09:00-10:00',
  '10:00-11:00',
  '11:00-12:00',
  '13:00-14:00',
  '14:00-15:00',
  '15:00-16:00',
  '16:00-17:00',
  '17:00-18:00',
  '18:00-19:00',
  '19:00-20:00',
];

  @override
  void initState() {
    super.initState();
    DebugLogger.ui('ResidentBookingFormScreen initialized');
    print('🔍 QR Code: Form screen initialized - QR code should be visible');
    _initializeForm();
  }

  // Helper function to convert 24h format to 12h format for display
  String _formatTimeForDisplay(String timeslot) {
    final parts = timeslot.split('-');
    final startTime = parts[0];
    final endTime = parts[1];
    
    String formatHour(String hour) {
      final h = int.parse(hour.split(':')[0]);
      final period = h >= 12 ? 'PM' : 'AM';
      final displayHour = h == 0 ? 12 : (h > 12 ? h - 12 : h);
      return '$displayHour:00 $period';
    }
    
    return '${formatHour(startTime)} - ${formatHour(endTime)}';
  }

  Future<void> _initializeForm() async {
    try {
      final authApiService = AuthApiService();
      final currentUser = authApiService.currentUser;
      print('🔍 Current user from server: $currentUser');
      
      if (currentUser != null) {
        setState(() {
          _nameController.text = currentUser['fullName'] ?? '';
          _contactController.text = currentUser['contactNumber'] ?? '';
          _addressController.text = currentUser['address'] ?? '';
        });
      }
    } catch (e) {
      print('🔥 Error initializing form: $e');
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _contactController.dispose();
    _addressController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    try {
      final XFile? pickedFile = await _imagePicker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1920,
        imageQuality: 85,
      );

      if (pickedFile != null) {
        print('🔍 DEBUG: Image picked - path: ${pickedFile.path}');
        try {
          final file = File(pickedFile.path);
          if (await file.exists()) {
            setState(() {
              _receiptImage = file;
            });
            print('✅ DEBUG: Receipt image file created successfully');
          } else {
            print('❌ DEBUG: Image file does not exist at path: ${pickedFile.path}');
          }
        } catch (e) {
          print('❌ DEBUG: Error creating File from XFile: $e');
        }
      }
    } catch (e) {
      print('❌ Error uploading images: $e');
      setState(() {
        _errorMessage = 'Failed to pick image: $e';
      });
    }
  }

  Future<String?> _uploadReceipt(File imageFile) async {
    try {
      final authApiService = AuthApiService();
      final currentUser = authApiService.currentUser;
      if (currentUser == null) {
        print('❌ No user logged in - cannot upload receipt');
        return null;
      }

      print('🌤️ Starting receipt upload for user: ${currentUser['email']}');
      print('🌤️ Image file path: ${imageFile.path}');

      // Upload receipt as Base64 to Firestore (FREE method)
      final bookingId = DateTime.now().millisecondsSinceEpoch.toString();
      
      final receiptBase64 = await Base64ImageService.uploadReceipt(
        receiptImage: imageFile,
        bookingId: bookingId,
      );
      
      if (receiptBase64 != null) {
        print('✅ Receipt converted to base64 successfully');
        print('📊 Base64 size: ${(receiptBase64.length / 1024).toStringAsFixed(2)} KB');
        return receiptBase64;
      } else {
        print('❌ Receipt base64 conversion failed');
        return null;
      }
    } catch (e) {
      print('🌤️ Receipt upload error: $e');
      return null;
    }
  }

  // Launch GCash payment process
  Future<void> _launchGCashPayment() async {
    try {
      // Show payment instructions dialog
      final confirmed = await showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('GCash Payment'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'You will be redirected to GCash to complete the payment.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue.shade200),
                ),
                child: const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Payment Steps:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text('1. You will be redirected to GCash'),
                    Text('2. Complete the payment'),
                    Text('3. Screenshot the payment receipt'),
                    Text('4. Return here to upload the receipt'),
                  ],
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pop(context, true),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
              child: const Text('Continue to GCash'),
            ),
          ],
        ),
      );

      if (confirmed == true) {
        // For now, we'll simulate the redirect
        // In a real implementation, you would use:
        // 1. URL launcher for GCash deep link
        // 2. Or open GCash app if available
        
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Opening GCash... (Simulated)'),
            backgroundColor: Colors.blue,
            duration: Duration(seconds: 2),
          ),
        );

        // Simulate waiting for payment
        await Future.delayed(const Duration(seconds: 2));

        // Show receipt upload prompt
        if (mounted) {
          _showReceiptUploadPrompt();
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error launching GCash: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  // Show receipt upload prompt after payment
  void _showReceiptUploadPrompt() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Upload Payment Receipt'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.receipt_long,
              size: 48,
              color: Colors.green,
            ),
            SizedBox(height: 16),
            Text(
              'Please upload your GCash payment receipt to complete the booking.',
              textAlign: TextAlign.center,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _pickImage(); // Open image picker
            },
            child: const Text('Upload Receipt'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  Future<void> _submitBooking() async {
    try {
      print('🔍 DEBUG: Submit button clicked');
      print('🔍 DEBUG: Selected timeslot: $_selectedTimeslot');
      
      if (!_formKey.currentState!.validate()) {
        print('🔍 DEBUG: Form validation failed');
        return;
      }

      print('🔍 DEBUG: Form validation passed');

      if (_selectedTimeslot == null) {
        print('🔍 DEBUG: No timeslot selected - showing error');
        setState(() {
          _errorMessage = 'Please select a timeslot';
        });
        return;
      }

      print('🔍 DEBUG: Timeslot validation passed');

      if (_receiptImage == null) {
        print('🔍 DEBUG: No receipt uploaded - showing error');
        setState(() {
          _errorMessage = 'Please upload a payment receipt';
        });
        return;
      }

      print('🔍 DEBUG: Receipt validation passed - proceeding to availability check');

      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });

      try {
        print('🔍 Checking time slot availability...');
        print('🔍 DEBUG: About to call _checkTimeSlotAvailability()');
        
        // First check if the time slot is available
        final availabilityResult = await _checkTimeSlotAvailability();
        print('🔍 DEBUG: _checkTimeSlotAvailability() returned: $availabilityResult');
        
        if (!availabilityResult['available']) {
          print('🔍 DEBUG: Time slot not available - showing error');
          setState(() {
            _errorMessage = availabilityResult['message'];
            _isLoading = false;
          });
          return;
        }
        
        print('🔍 DEBUG: Time slot is available - proceeding');
      
      // Show competitive booking warning if applicable
      if (availabilityResult['is_competitive'] == true) {
        final shouldProceed = await _showCompetitiveBookingWarning();
        if (!shouldProceed) {
          setState(() {
            _isLoading = false;
          });
          return;
        }
      }
      
      print('✅ Time slot is available, submitting booking...');
      
      // Upload receipt first if available
      String? receiptImageUrl;
      if (_receiptImage != null) {
        receiptImageUrl = await _uploadReceipt(_receiptImage!);
        if (receiptImageUrl == null) {
          throw Exception('Failed to upload receipt image');
        }
      }

      // Create payment details
      final paymentDetails = {
        'gcashNumber': _gcashNumberController.text.trim(),
        'gcashName': _gcashNameController.text.trim(),
        'email': _gcashEmailController.text.trim(),
        'receiptDetails': _receiptDetailsController.text.trim(),
      };

      // Submit booking via Server API
      print('🔍 DEBUG: About to submit booking with receipt data');
      print('🔍 DEBUG: receiptImageUrl: $receiptImageUrl');
      print('🔍 DEBUG: receiptImageUrl length: ${receiptImageUrl?.length ?? 0}');
      
      final result = await ApiService.createBooking({
        'facility_id': widget.facilityId,
        'facility_name': widget.facilityName,
        'date': widget.selectedDate,
        'timeslot': _selectedTimeslot!,
        'purpose': _purposeController.text.trim(),
        'payment_details': paymentDetails,
        'receipt_base64': receiptImageUrl, // Use receipt_base64 instead of receipt_image_url
        'user_id': currentUser['id'],
        'user_name': currentUser['fullName'],
        'user_email': currentUser['email'],
        'user_contact': currentUser['contactNumber'] ?? '',
        'status': 'pending',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      });
      
      print('🔍 DEBUG: Booking submission result: $result');

      if (result['success']) {
        print('✅ Booking submitted successfully!');
        
        // Show success message with competitive booking info
        if (mounted) {
          String message = result['message'] ?? 'Booking submitted successfully!';
          if (result['note'] != null) {
            message += '\n\n${result['note']}';
          }
          
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(message),
              backgroundColor: Colors.green,
              duration: const Duration(seconds: 4),
              action: SnackBarAction(
                label: 'View Status',
                textColor: Colors.white,
                onPressed: () {
                  Navigator.pop(context); // Go back to calendar
                  if (widget.onBookingSubmitted != null) {
                    widget.onBookingSubmitted!();
                  }
                },
              ),
            ),
          );
          Navigator.pop(context); // Go back to calendar
          if (widget.onBookingSubmitted != null) {
            widget.onBookingSubmitted!();
          }
        }
      } else {
        // Handle server validation errors
        setState(() {
          _errorMessage = result['message'] ?? 'Failed to submit booking';
          _isLoading = false;
        });
      }
    } catch (e) {
      print('❌ Booking submission error: $e');
      if (mounted) {
        setState(() {
          _errorMessage = 'Failed to submit booking: $e';
          _isLoading = false;
        });
      }
    }
    } catch (e) {
      print('❌ CRITICAL ERROR in _submitBooking: $e');
      print('❌ Stack trace: ${StackTrace.current}');
      if (mounted) {
        setState(() {
          _errorMessage = 'Critical error: $e';
          _isLoading = false;
        });
      }
    }
  }

  Future<Map<String, dynamic>> _checkTimeSlotAvailability() async {
    try {
      print('🔍 DEBUG: Checking availability for facility ${widget.facilityId}, date ${widget.selectedDate}, user ${currentUser['email']}');
      print('🔍 DEBUG: Selected timeslot: $_selectedTimeslot');
      
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/available-timeslots?facility_id=${widget.facilityId}&date=${widget.selectedDate}&user_email=${currentUser['email']}'),
        headers: {'Content-Type': 'application/json'},
      );

      print('🔍 DEBUG: Response status: ${response.statusCode}');
      print('🔍 DEBUG: Response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success']) {
          final availableSlots = List<String>.from(data['available_timeslots']);
          final userBookedSlots = List<String>.from(data['user_booked_timeslots']);
          final competitiveSlots = List<String>.from(data['competitive_timeslots']);
          final approvedSlots = List<String>.from(data['approved_timeslots']);
          
          print('🔍 DEBUG: Available slots: $availableSlots');
          print('🔍 DEBUG: User booked slots: $userBookedSlots');
          print('🔍 DEBUG: Competitive slots: $competitiveSlots');
          print('🔍 DEBUG: Approved slots: $approvedSlots');
          print('🔍 DEBUG: Selected timeslot: $_selectedTimeslot');
          
          // Check if the selected time slot is available for booking
          if (userBookedSlots.contains(_selectedTimeslot)) {
            print('🔍 DEBUG: User already booked this slot');
            return {
              'available': false,
              'message': 'You already have a booking for this time slot. Please choose a different time.'
            };
          } else if (approvedSlots.contains(_selectedTimeslot)) {
            print('🔍 DEBUG: Slot is already approved/taken');
            return {
              'available': false,
              'message': 'This time slot is already taken. Please choose a different time.'
            };
          } else if (competitiveSlots.contains(_selectedTimeslot)) {
            print('🔍 DEBUG: Slot is competitive');
            // Allow competitive booking
            return {
              'available': true,
              'message': 'Competitive booking: Multiple users may book this time slot. First approved wins!',
              'is_competitive': true
            };
          } else if (availableSlots.contains(_selectedTimeslot)) {
            print('🔍 DEBUG: Slot is available');
            return {
              'available': true,
              'message': 'Time slot is available',
              'is_competitive': false
            };
          } else {
            print('🔍 DEBUG: Slot is not available for unknown reason');
            return {
              'available': false,
              'message': 'This time slot is not available. Please choose a different time.'
            };
          }
        }
      }
      
      return {'available': false, 'message': 'Could not verify time slot availability'};
    } catch (e) {
      print('❌ Error checking availability: $e');
      return {'available': false, 'message': 'Error checking availability: $e'};
    }
  }

  Future<bool> _showCompetitiveBookingWarning() async {
    return await showDialog<bool>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Row(
            children: [
              Icon(Icons.warning, color: Colors.orange),
              SizedBox(width: 8),
              Text('Competitive Booking'),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '⚠️ This time slot is competitive!',
                style: TextStyle(fontWeight: FontWeight.bold, color: Colors.orange),
              ),
              SizedBox(height: 12),
              Text('Multiple users may book the same time slot. The first booking to get approved wins!'),
              SizedBox(height: 8),
              Text('Other users may also be trying to book this time slot.'),
              SizedBox(height: 12),
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue[200]!),
                ),
                child: Row(
                  children: [
                    Icon(Icons.info, color: Colors.blue, size: 20),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Your booking will be submitted as pending. An official will review and approve bookings.',
                        style: TextStyle(fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.of(context).pop(true),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange,
                foregroundColor: Colors.white,
              ),
              child: Text('Proceed Anyway'),
            ),
          ],
        );
      },
    ) ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Book ${widget.facilityName}'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Facility and Date Info
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.blue.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Facility: ${widget.facilityName}',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Date: ${widget.selectedDate}',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Rate: ₱${widget.facilityRate}/hour',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 16),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Personal Information
              const Text(
                'Personal Information',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Full Name',
                  hintText: 'Enter your full name',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter your full name';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _contactController,
                decoration: const InputDecoration(
                  labelText: 'Contact Number',
                  hintText: 'Enter your contact number',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.phone),
                ),
                keyboardType: TextInputType.phone,
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter your contact number';
                  }
                  if (value.trim().length < 10) {
                    return 'Please enter a valid contact number';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _addressController,
                decoration: const InputDecoration(
                  labelText: 'Address',
                  hintText: 'Enter your complete address',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.home),
                ),
                maxLines: 2,
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter your address';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),

              // Timeslot Selection
              const Text(
                'Select Timeslot',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey.shade300),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Available Timeslots:',
                      style: TextStyle(
                        fontWeight: FontWeight.w500,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 12),
                    ..._timeslots.map((timeslot) {
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: InkWell(
                          onTap: () {
                            print('🔍 DEBUG: User selected timeslot: $timeslot');
                            setState(() {
                              _selectedTimeslot = timeslot;
                            });
                          },
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: _selectedTimeslot == timeslot
                                  ? Colors.blue.shade100
                                  : Colors.grey.shade100,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: _selectedTimeslot == timeslot
                                    ? Colors.blue
                                    : Colors.grey.shade300,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  _selectedTimeslot == timeslot
                                      ? Icons.radio_button_checked
                                      : Icons.radio_button_unchecked,
                                  color: _selectedTimeslot == timeslot
                                      ? Colors.blue
                                      : Colors.grey,
                                ),
                                const SizedBox(width: 12),
                                Text(
                                  _formatTimeForDisplay(timeslot),
                                  style: TextStyle(
                                    fontWeight: _selectedTimeslot == timeslot
                                        ? FontWeight.bold
                                        : FontWeight.normal,
                                    color: _selectedTimeslot == timeslot
                                        ? Colors.blue
                                        : Colors.black87,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    }),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // GCash Payment Section
              const Text(
                'Payment Information',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.blue.shade200),
                  borderRadius: BorderRadius.circular(12),
                  color: Colors.blue.shade50,
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        // QR Code Container - Now Tappable
                        GestureDetector(
                          onTap: () {
                            print('🔍 QR Code: QR code tapped!');
                            _launchGCashPayment();
                          },
                          child: Container(
                            width: 80,
                            height: 80,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.blue.shade300),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.blue.withOpacity(0.1),
                                  blurRadius: 4,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: Stack(
                              children: [
                                // QR Code Image with fallback
                                Container(
                                  width: double.infinity,
                                  height: double.infinity,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(8),
                                    color: Colors.white,
                                  ),
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(8),
                                    child: Image.asset(
                                      'assets/images/qr_codes/qr-code-merchant-image.jpg',
                                      fit: BoxFit.cover,
                                      errorBuilder: (context, error, stackTrace) {
                                        print('❌ QR Code image load error: $error');
                                        return const Icon(
                                          Icons.qr_code_2,
                                          size: 40,
                                          color: Colors.blue,
                                        );
                                      },
                                    ),
                                  ),
                                ),
                                // Tap indicator
                                Positioned(
                                  bottom: 2,
                                  right: 2,
                                  child: Container(
                                    width: 16,
                                    height: 16,
                                    decoration: BoxDecoration(
                                      color: Colors.green,
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: const Icon(
                                      Icons.touch_app,
                                      size: 10,
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Tap QR Code to Pay with GCash',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blue,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Merchant: Barangay Reserve',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.black87,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Amount: ₱${widget.facilityRate}/hour',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.black87,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.green.shade50,
                                  borderRadius: BorderRadius.circular(6),
                                  border: Border.all(color: Colors.green.shade200),
                                ),
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.info_outline,
                                      size: 16,
                                      color: Colors.green.shade700,
                                    ),
                                    const SizedBox(width: 6),
                                    Expanded(
                                      child: Text(
                                        'Tap QR code → Pay in GCash → Screenshot receipt → Return here',
                                        style: TextStyle(
                                          fontSize: 12,
                                          color: Colors.green.shade700,
                                          fontWeight: FontWeight.w500,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.blue.shade100,
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Text(
                        '💡 Please pay the exact amount and upload the receipt below',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.blue,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Receipt Upload
              const Text(
                'Payment Receipt',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              InkWell(
                onTap: _pickImage,
                child: Container(
                  width: double.infinity,
                  height: 150,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey.shade300),
                    borderRadius: BorderRadius.circular(12),
                    color: Colors.grey.shade50,
                  ),
                  child: _receiptImage != null
                      ? Stack(
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(12),
                              child: Image.file(
                                _receiptImage!,
                                width: double.infinity,
                                height: double.infinity,
                                fit: BoxFit.cover,
                              ),
                            ),
                            Positioned(
                              top: 8,
                              right: 8,
                              child: Container(
                                decoration: BoxDecoration(
                                  color: Colors.black54,
                                  shape: BoxShape.circle,
                                ),
                                child: IconButton(
                                  icon: const Icon(
                                    Icons.close,
                                    color: Colors.white,
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      _receiptImage = null;
                                    });
                                  },
                                ),
                              ),
                            ),
                          ],
                        )
                      : Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.cloud_upload,
                              size: 48,
                              color: Colors.grey.shade400,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Tap to upload receipt',
                              style: TextStyle(
                                color: Colors.grey.shade600,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Text(
                              'JPG, PNG (Max 5MB)',
                              style: TextStyle(
                                color: Colors.grey.shade500,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                ),
              ),
              const SizedBox(height: 32),

              // Error Message
              if (_errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error, color: Colors.red.shade600),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _errorMessage!,
                          style: TextStyle(color: Colors.red.shade600),
                        ),
                      ),
                    ],
                  ),
                ),
              const SizedBox(height: 16),

              // Submit Button
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _submitBooking,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                              ),
                            ),
                            SizedBox(width: 12),
                            Text('Submitting...'),
                          ],
                        )
                      : const Text(
                          'Submit Booking',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
