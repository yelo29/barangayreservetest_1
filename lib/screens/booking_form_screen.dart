import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/api_service.dart';

class BookingFormScreen extends StatefulWidget {
  final Map<String, dynamic> facility;
  final DateTime selectedDate;
  final Map<String, dynamic>? userData;

  const BookingFormScreen({
    Key? key,
    required this.facility,
    required this.selectedDate,
    this.userData,
  }) : super(key: key);

  @override
  State<BookingFormScreen> createState() => _BookingFormScreenState();
}

class _BookingFormScreenState extends State<BookingFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _contactController = TextEditingController();
  final _addressController = TextEditingController();
  final _purposeController = TextEditingController();
  final _receiptDetailsController = TextEditingController();
  
  String _selectedTimeSlot = '';
  File? _receiptImage;
  bool _isLoading = false;
  bool _isLoadingTimeSlots = true;
  
  List<String> _timeSlots = [
    '6:00 AM - 8:00 AM',
    '8:00 AM - 10:00 AM',
    '10:00 AM - 12:00 PM',
    '12:00 PM - 2:00 PM',
    '2:00 PM - 4:00 PM',
    '4:00 PM - 6:00 PM',
    '6:00 PM - 8:00 PM',
    '8:00 PM - 10:00 PM',
  ];

  @override
  void initState() {
    super.initState();
    _loadTimeSlotAvailability();
  }

  // Helper method to check if current user is an official
  bool get _isOfficial {
    final String currentUserEmail = widget.userData?['email'] ?? '';
    return currentUserEmail.contains('official') || 
           currentUserEmail.contains('barangay') ||
           currentUserEmail.contains('admin');
  }

  Future<void> _loadTimeSlotAvailability() async {
    if (mounted) {
      setState(() {
        _isLoadingTimeSlots = true;
      });
    }

    try {
      print('🔍 Loading time slot availability for date: ${widget.selectedDate.toIso8601String().split('T')[0]}');
      
      // Add timeout to prevent infinite loading
      final response = await ApiService.getTimeSlots(
        widget.facility['id'],
        widget.selectedDate.toIso8601String().split('T')[0]
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception('Time slot loading timed out after 10 seconds');
        },
      );
      
      if (response['success'] == true) {
        final List<dynamic> availableSlots = response['available_slots'] ?? [];
        print('🔍 BookingFormScreen - Received ${availableSlots.length} available time slots');
        
        if (mounted) {
          setState(() {
            _timeSlots = availableSlots.cast<String>();
            _isLoadingTimeSlots = false;
          });
        }
      } else {
        print('🔍 BookingFormScreen - Failed to load time slots: ${response['error']}');
        if (mounted) {
          setState(() {
            _isLoadingTimeSlots = false;
          });
        }
      }
    } catch (e) {
      print('🔍 BookingFormScreen - Error loading time slots: $e');
      if (mounted) {
        setState(() {
          _isLoadingTimeSlots = false;
        });
      }
    }
  }

  Future<void> _pickImage() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(source: ImageSource.gallery);
      
      if (image != null) {
        setState(() {
          _receiptImage = File(image.path);
        });
        
        // Read image and convert to base64
        final bytes = await image.readAsBytes();
        final base64String = base64Encode(bytes);
        
        setState(() {
          _receiptDetailsController.text = 'Receipt uploaded (${bytes.length} bytes)';
        });
        
        print('🔍 Image uploaded and converted to base64 (${bytes.length} bytes)');
      }
    } catch (e) {
      print('🔍 Error picking image: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error picking image: $e')),
      );
    }
  }

  Future<void> _submitBooking() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }
    
    if (_selectedTimeSlot.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a time slot')),
      );
      return;
    }
    
    if (!_isOfficial && _receiptImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please upload a payment receipt'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }
    
    setState(() {
      _isLoading = true;
    });

    try {
      // Prepare booking data
      Map<String, dynamic> bookingData = {
        'facility_id': widget.facility['id'],
        'user_email': widget.userData?['email'] ?? 'user@example.com',
        'date': widget.selectedDate.toIso8601String().split('T')[0],
        'timeslot': _selectedTimeSlot,
        'total_amount': widget.facility['hourly_rate'] ?? widget.facility['rate'] ?? widget.facility['price'] ?? widget.facility['base_rate'] ?? 0,
        'status': _isOfficial ? 'approved' : 'pending', // Officials get auto-approved
      };

      // Add personal information only for residents
      if (!_isOfficial) {
        bookingData['full_name'] = _nameController.text;
        bookingData['contact_number'] = _contactController.text;
        bookingData['address'] = _addressController.text;
        bookingData['purpose'] = _purposeController.text;
        
        // Add receipt if uploaded
        if (_receiptImage != null) {
          final bytes = await _receiptImage!.readAsBytes();
          final base64String = base64Encode(bytes);
          bookingData['receipt_base64'] = 'data:image/jpeg;base64,$base64String';
        }
      }

      final response = await ApiService.createBooking(bookingData);
      
      if (response['success'] == true) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(_isOfficial ? 'Official booking created successfully!' : 'Booking submitted successfully!'),
            backgroundColor: Colors.green,
          ),
        );
        
        // Clear form and go back
        _formKey.currentState!.reset();
        Navigator.of(context).pop();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(response['message'] ?? 'Failed to submit booking'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      print('🔍 Error submitting booking: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error submitting booking: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Book ${widget.facility['name']}'),
        backgroundColor: Colors.blue.shade700,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Facility Information
              Container(
                padding: const EdgeInsets.all(16),
                margin: const EdgeInsets.only(bottom: 16),
                decoration: BoxDecoration(
                  color: Colors.grey[50],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Facility Information',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue.shade700,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Date: ${widget.selectedDate.toString().split(' ')[0]}',
                      style: const TextStyle(fontSize: 16),
                    ),
                    Text(
                      'Selected Time: $_selectedTimeSlot',
                      style: const TextStyle(fontSize: 16),
                    ),
                  ],
                ),
              ),
              
              // Time Slot Selection
              if (_isLoadingTimeSlots)
                const Center(child: CircularProgressIndicator())
              else
                Container(
                  padding: const EdgeInsets.all(16),
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: Colors.grey[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Select Time Slot',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue.shade700,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: _timeSlots.map((slot) {
                          final isSelected = _selectedTimeSlot == slot;
                          return ChoiceChip(
                            label: Text(slot),
                            selected: isSelected,
                            onSelected: (selected) {
                              setState(() {
                                _selectedTimeSlot = selected ? slot : '';
                              });
                            },
                            backgroundColor: isSelected ? Colors.blue.shade700 : Colors.grey[300],
                            labelStyle: TextStyle(
                              color: isSelected ? Colors.white : Colors.black87,
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),
              
              // Personal Information (only for residents)
              if (!_isOfficial) ...[
                Container(
                  padding: const EdgeInsets.all(16),
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: Colors.grey[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Personal Information',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _nameController,
                        decoration: const InputDecoration(
                          labelText: 'Full Name',
                          border: OutlineInputBorder(),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
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
                          border: OutlineInputBorder(),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your contact number';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _addressController,
                        decoration: const InputDecoration(
                          labelText: 'Address',
                          border: OutlineInputBorder(),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your address';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _purposeController,
                        decoration: const InputDecoration(
                          labelText: 'Purpose',
                          border: OutlineInputBorder(),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter the purpose of booking';
                          }
                          return null;
                        },
                      ),
                    ],
                  ),
                ),
              ],
              
              // Receipt Upload (only for residents)
              if (!_isOfficial) ...[
                Container(
                  padding: const EdgeInsets.all(16),
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: Colors.grey[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Payment Receipt',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),
                      GestureDetector(
                        onTap: _pickImage,
                        child: Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey[300]!),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Row(
                            children: [
                              Icon(Icons.upload_file, color: Colors.grey[600]),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  _receiptImage != null 
                                      ? 'Receipt uploaded (${_receiptImage!.path.split('/').last})'
                                      : 'Tap to upload payment receipt',
                                  style: TextStyle(
                                    color: _receiptImage != null ? Colors.green : Colors.grey[600],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      if (_receiptImage != null)
                        Container(
                          margin: const EdgeInsets.only(top: 8),
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: Colors.green[50],
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            '✓ Receipt uploaded',
                            style: TextStyle(
                              color: Colors.green[700],
                              fontSize: 12,
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ],
              
              // Submit Button
              Container(
                width: double.infinity,
                margin: const EdgeInsets.only(top: 16),
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _submitBooking,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue.shade700,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Text('Submit Booking'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
