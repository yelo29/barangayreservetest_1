import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

// Define the BarangayEvent class
class BarangayEvent {
  final String eventName;
  final DateTime date;

  BarangayEvent({
    required this.eventName,
    required this.date,
  });
}

class OfficialEventForm extends StatefulWidget {
  const OfficialEventForm({super.key});

  @override
  _OfficialEventFormState createState() => _OfficialEventFormState();
}

class _OfficialEventFormState extends State<OfficialEventForm> {
  final _formKey = GlobalKey<FormState>();
  String _eventName = '';
  DateTime? _selectedDate;

  // Define the addBarangayEvent method
  void addBarangayEvent(BarangayEvent event) {
    // For now, we'll just show a success message
    // In a real app, you would save this to your database or state management
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Event "${event.eventName}" booked successfully!')),
    );
    
    // You can add your logic here to save the event to your data store
    // For example:
    // eventsList.add(event);
    // setState(() {}); // if you need to update the UI
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      if (_selectedDate != null) {
        // Create a new BarangayEvent
        final newEvent = BarangayEvent(
          eventName: _eventName,
          date: _selectedDate!,
        );

        // Add the event to your data source
        addBarangayEvent(newEvent);

        Navigator.of(context).pop();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Please select a date')),
        );
      }
    }
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate ?? DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2101),
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Book Barangay Event'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: <Widget>[
              TextFormField(
                decoration: const InputDecoration(labelText: 'Event Name'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter an event name';
                  }
                  return null;
                },
                onSaved: (value) {
                  _eventName = value!;
                },
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    child: Text(
                      _selectedDate == null
                          ? 'No date chosen!'
                          : 'Selected Date: ${DateFormat.yMd().format(_selectedDate!)}',
                    ),
                  ),
                  TextButton(
                    onPressed: () => _selectDate(context),
                    child: const Text('Choose Date'),
                  ),
                ],
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: _submitForm,
                child: const Text('Book Event'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
