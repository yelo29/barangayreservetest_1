class Facility {
  final String id;
  final String name;
  final String icon;
  final String rate;
  final String description;
  final String capacity;
  final String downpayment;
  final String amenities;

  Facility({
    required this.id,
    required this.name,
    required this.icon,
    required this.rate,
    required this.description,
    required this.capacity,
    required this.downpayment,
    required this.amenities,
  });

  // Empty constructor for fallback
  Facility.empty()
      : id = '',
        name = '',
        icon = '',
        rate = '',
        description = '',
        capacity = '',
        downpayment = '',
        amenities = '';

  factory Facility.fromMap(Map<String, dynamic> map) {
    return Facility(
      id: map['id']?.toString() ?? '',
      name: map['name']?.toString() ?? '',
      icon: map['icon']?.toString() ?? '',
      rate: map['rate']?.toString() ?? '',
      description: map['description']?.toString() ?? '',
      capacity: map['capacity']?.toString() ?? '',
      downpayment: map['downpayment']?.toString() ?? '',
      amenities: map['amenities']?.toString() ?? '',
    );
  }
}
