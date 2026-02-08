import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class EnhancedCalendar extends StatefulWidget {
  final DateTime selectedDate;
  final Function(DateTime) onDateSelected;
  final Map<String, String>? bookingStatuses;
  final bool Function(DateTime)? isDateEnabled;
  final Color? selectedColor;
  final Color? availableColor;
  final Color? pendingColor;
  final Color? bookedColor;
  final Color? eventColor;
  final bool showWeekNumbers;
  final bool showTodayButton;
  final DateTime? firstDate;
  final DateTime? lastDate;
  final String? currentUserEmail;
  final String? currentUserRole;

  const EnhancedCalendar({
    super.key,
    required this.selectedDate,
    required this.onDateSelected,
    this.bookingStatuses,
    this.isDateEnabled,
    this.selectedColor,
    this.availableColor,
    this.pendingColor,
    this.bookedColor,
    this.eventColor,
    this.showWeekNumbers = false,
    this.showTodayButton = true,
    this.firstDate,
    this.lastDate,
    this.currentUserEmail,
    this.currentUserRole,
  });

  @override
  State<EnhancedCalendar> createState() => _EnhancedCalendarState();
}

class _EnhancedCalendarState extends State<EnhancedCalendar> {
  late DateTime _currentMonth;
  late DateTime _selectedDate;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _currentMonth = DateTime(widget.selectedDate.year, widget.selectedDate.month, 1);
    _selectedDate = widget.selectedDate;
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _previousMonth() {
    setState(() {
      _currentMonth = DateTime(_currentMonth.year, _currentMonth.month - 1);
    });
  }

  void _nextMonth() {
    setState(() {
      _currentMonth = DateTime(_currentMonth.year, _currentMonth.month + 1);
    });
  }

  void _goToToday() {
    final DateTime today = DateTime.now();
    setState(() {
      _currentMonth = DateTime(today.year, today.month, 1);
      _selectedDate = today;
    });
    widget.onDateSelected(today);
  }

  void _goToMonth(DateTime month) {
    setState(() {
      _currentMonth = DateTime(month.year, month.month, 1);
    });
  }

  bool _isDateEnabled(DateTime date) {
    if (widget.isDateEnabled != null) {
      return widget.isDateEnabled!(date);
    }
    
    // 🔥 ROLE-SPECIFIC LOGIC: Different behavior for residents vs officials
    final String dateKey = '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
    final String? status = widget.bookingStatuses?[dateKey];
    
    print('🔍 Calendar date check: $dateKey -> status: $status');
    
    // Disable dates with official bookings (gray - untappable for everyone)
    if (status == 'official_locked' || status == 'official_unavailable') {
      print('🔍 Date $dateKey is LOCKED (official booking) - disabled for ALL users');
      return false; // Official bookings lock calendar for everyone
    }
    
    // For resident approved bookings, check if this is handled at calendar level
    // Note: If status is 'approved', it means OTHER resident's booking (current user's own bookings use 'own_approved')
    if (status == 'approved') {
      // Check if current user is an official
      final bool isOfficial = widget.currentUserRole?.toString().toLowerCase() == 'official' ||
                             widget.currentUserEmail?.toString().contains('official') == true ||
                             widget.currentUserEmail?.toString().contains('barangay') == true ||
                             widget.currentUserEmail?.toString().contains('admin') == true;
      
      if (isOfficial) {
        print('🔍 DEBUG: Date $dateKey has resident approved booking - OFFICIAL can override (enabled)');
        // Don't return false, continue to check past dates - officials can override resident bookings
      } else {
        print('🔍 DEBUG: Date $dateKey has OTHER resident approved booking - disabled');
        return false; // Other resident approved bookings lock calendar for residents
      }
    }
    
    // User's own approved bookings are tappable (green but available)
    if (status == 'own_approved') {
      print('🔍 DEBUG: Date $dateKey has USER OWN approved booking - enabled (green)');
      // Don't return false here, continue to check past dates
    }
    
    // If status is null or not 'approved'/'official_locked', check past dates
    print('🔍 DEBUG: Date $dateKey is available for booking');
    
    // Default: disable past dates
    final DateTime today = DateTime.now();
    final DateTime todayDateOnly = DateTime(today.year, today.month, today.day);
    final DateTime dateOnly = DateTime(date.year, date.month, date.day);
    
    return !dateOnly.isBefore(todayDateOnly);
  }

  Color _getDateColor(DateTime date) {
    // Use the same format as facility calendar screen
    final String dateKey = '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
    final String? status = widget.bookingStatuses?[dateKey];

    switch (status) {
      case 'event':
        return widget.eventColor ?? Colors.green;
      case 'approved':
        return widget.bookedColor ?? Colors.green; // Green for resident-approved bookings
      case 'own_approved':
        return widget.bookedColor ?? Colors.green; // Green for user's own approved bookings (tappable)
      case 'pending':
        return widget.pendingColor ?? Colors.yellow; // Yellow for resident-pending bookings
      case 'official_locked':
        return Colors.grey.shade400; // Gray for official bookings (locked for everyone)
      case 'official':
        return Colors.grey.shade400; // Gray for official bookings (locked for everyone)
      case 'official_unavailable':
        return Colors.grey.shade400; // Gray for official bookings (locked for everyone)
      case 'available':
        return widget.availableColor ?? Colors.white; // White for available dates
      default:
        return widget.availableColor ?? Colors.white; // Default to white
    }
  }

  bool _isToday(DateTime date) {
    final DateTime today = DateTime.now();
    return date.day == today.day &&
           date.month == today.month &&
           date.year == today.year;
  }

  bool _isSelected(DateTime date) {
    return date.day == _selectedDate.day &&
           date.month == _selectedDate.month &&
           date.year == _selectedDate.year;
  }

  void _onDateTap(DateTime date) {
    if (_isDateEnabled(date)) {
      setState(() {
        _selectedDate = date;
      });
      widget.onDateSelected(date);
    }
  }

  Widget _buildMonthHeader() {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            onPressed: _previousMonth,
            icon: const Icon(Icons.chevron_left),
            tooltip: 'Previous Month',
          ),
          Expanded(
            child: GestureDetector(
              onTap: () => _showMonthPicker(),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Expanded(
                      child: Text(
                        DateFormat.yMMMM('en_US').format(_currentMonth),
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                        overflow: TextOverflow.ellipsis,
                        maxLines: 1,
                      ),
                    ),
                    const SizedBox(width: 4),
                    Icon(
                      Icons.arrow_drop_down,
                      color: Colors.grey.shade600,
                    ),
                  ],
                ),
              ),
            ),
          ),
          IconButton(
            onPressed: _nextMonth,
            icon: const Icon(Icons.chevron_right),
            tooltip: 'Next Month',
          ),
        ],
      ),
    );
  }

  Widget _buildWeekdayHeaders() {
    final List<String> weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: widget.showWeekNumbers
            ? <Widget>[
                // Week number header
                const SizedBox(width: 32),
                ...weekdays.map((day) => Expanded(
                  child: Center(
                    child: Text(
                      day,
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.grey.shade600,
                        fontSize: 12,
                      ),
                    ),
                  ),
                )),
              ]
            : weekdays.map((day) => Expanded(
                  child: Center(
                    child: Text(
                      day,
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.grey.shade600,
                        fontSize: 12,
                      ),
                    ),
                  ),
                )).toList(),
      ),
    );
  }

  Widget _buildCalendarGrid() {
    final int daysInMonth = DateUtils.getDaysInMonth(_currentMonth.year, _currentMonth.month);
    final DateTime firstDayOfMonth = DateTime(_currentMonth.year, _currentMonth.month, 1);
    final int startingWeekday = firstDayOfMonth.weekday % 7; // Sunday as 0
    final int totalCells = daysInMonth + startingWeekday;
    final int rows = (totalCells / 7).ceil();

      return Expanded(
      child: SingleChildScrollView(
      child: Column(
      children: List.generate(rows, (weekIndex) {
        final int startIndex = weekIndex * 7;

        return SizedBox(
          height: 55,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: Row(
              children: List.generate(7, (dayIndex) {
                final int cellIndex = startIndex + dayIndex;
                if (cellIndex >= totalCells) {
                  return const Expanded(child: SizedBox());
                }
                if (widget.showWeekNumbers && dayIndex == 0) {
                  final int weekNumber = ((startIndex - startingWeekday) / 7).ceil() + 1;
                  return SizedBox(
                    width: 28,
                    child: Center(
                      child: Text(
                        weekNumber.toString(),
                        style: TextStyle(
                          fontSize: 10,
                          color: Colors.grey.shade500,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  );
                }

                if (cellIndex < startingWeekday || cellIndex >= totalCells) {
                  return const Expanded(child: SizedBox.shrink());
                }

                final int day = cellIndex - startingWeekday + 1;
                final DateTime date = DateTime(_currentMonth.year, _currentMonth.month, day);
                final bool isEnabled = _isDateEnabled(date);
                final bool isToday = _isToday(date);
                final bool isSelected = _isSelected(date);
                final Color dateColor = _getDateColor(date);

                return Expanded(
                  child: GestureDetector(
                    onTap: isEnabled ? () => _onDateTap(date) : null,
                    child: Container(
                      margin: const EdgeInsets.all(2),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? (widget.selectedColor ?? Colors.blue)
                            : dateColor,
                        borderRadius: BorderRadius.circular(8),
                        border: isToday
                            ? Border.all(color: Colors.blue, width: 2)
                            : null,
                        boxShadow: isSelected
                            ? [
                                BoxShadow(
                                  color: Colors.blue.withValues(alpha: 0.3),
                                  blurRadius: 4,
                                  offset: const Offset(0, 2),
                                ),
                              ]
                            : null,
                      ),
                      child: Center(
                        child: Text(
                          '$day',
                          style: TextStyle(
                            color: isSelected
                              ? Colors.white
                              : isEnabled
                                  ? Colors.black87
                                  : Colors.grey,
                            fontWeight: isSelected || isToday
                                ? FontWeight.bold
                                : FontWeight.normal,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ),
                  ),
                );
              }),
            ),
          ),
        );
      }),
    ),
    ),
    );
  }

  void _showMonthPicker() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Select Month'),
        content: SizedBox(
          width: 300,
          height: 300,
          child: GridView.builder(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 3,
              childAspectRatio: 2,
            ),
            itemCount: 12,
            itemBuilder: (context, index) {
              final DateTime month = DateTime(_currentMonth.year, index + 1, 1);
              final bool isSelected = month.month == _currentMonth.month;
              
              return GestureDetector(
                onTap: () {
                  Navigator.pop(context);
                  _goToMonth(month);
                },
                child: Container(
                  margin: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    color: isSelected
                        ? Theme.of(context).primaryColor
                        : Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Text(
                      DateFormat.MMM('en_US').format(month),
                      style: TextStyle(
                        color: isSelected ? Colors.white : Colors.black87,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildMonthHeader(),
        _buildWeekdayHeaders(),
        const SizedBox(height: 8),
        _buildCalendarGrid(),
        const SizedBox(height: 16),
      ],
    );
  }
}
