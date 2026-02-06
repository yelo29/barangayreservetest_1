part of 'generated.dart';

class ListEventsForUserVariablesBuilder {
  
  final FirebaseDataConnect _dataConnect;
  ListEventsForUserVariablesBuilder(this._dataConnect, );
  Deserializer<ListEventsForUserData> dataDeserializer = (dynamic json)  => ListEventsForUserData.fromJson(jsonDecode(json));
  
  Future<QueryResult<ListEventsForUserData, void>> execute() {
    return ref().execute();
  }

  QueryRef<ListEventsForUserData, void> ref() {
    
    return _dataConnect.query("ListEventsForUser", dataDeserializer, emptySerializer, null);
  }
}

@immutable
class ListEventsForUserEvents {
  final String id;
  final String name;
  final String description;
  final String location;
  final Timestamp eventDate;
  final String? category;
  final String? contactInfo;
  final String? imageUrl;
  ListEventsForUserEvents.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']),
  name = nativeFromJson<String>(json['name']),
  description = nativeFromJson<String>(json['description']),
  location = nativeFromJson<String>(json['location']),
  eventDate = Timestamp.fromJson(json['eventDate']),
  category = json['category'] == null ? null : nativeFromJson<String>(json['category']),
  contactInfo = json['contactInfo'] == null ? null : nativeFromJson<String>(json['contactInfo']),
  imageUrl = json['imageUrl'] == null ? null : nativeFromJson<String>(json['imageUrl']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final ListEventsForUserEvents otherTyped = other as ListEventsForUserEvents;
    return id == otherTyped.id && 
    name == otherTyped.name && 
    description == otherTyped.description && 
    location == otherTyped.location && 
    eventDate == otherTyped.eventDate && 
    category == otherTyped.category && 
    contactInfo == otherTyped.contactInfo && 
    imageUrl == otherTyped.imageUrl;
    
  }
  @override
  int get hashCode => Object.hashAll([id.hashCode, name.hashCode, description.hashCode, location.hashCode, eventDate.hashCode, category.hashCode, contactInfo.hashCode, imageUrl.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    json['name'] = nativeToJson<String>(name);
    json['description'] = nativeToJson<String>(description);
    json['location'] = nativeToJson<String>(location);
    json['eventDate'] = eventDate.toJson();
    if (category != null) {
      json['category'] = nativeToJson<String?>(category);
    }
    if (contactInfo != null) {
      json['contactInfo'] = nativeToJson<String?>(contactInfo);
    }
    if (imageUrl != null) {
      json['imageUrl'] = nativeToJson<String?>(imageUrl);
    }
    return json;
  }

  ListEventsForUserEvents({
    required this.id,
    required this.name,
    required this.description,
    required this.location,
    required this.eventDate,
    this.category,
    this.contactInfo,
    this.imageUrl,
  });
}

@immutable
class ListEventsForUserData {
  final List<ListEventsForUserEvents> events;
  ListEventsForUserData.fromJson(dynamic json):
  
  events = (json['events'] as List<dynamic>)
        .map((e) => ListEventsForUserEvents.fromJson(e))
        .toList();
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final ListEventsForUserData otherTyped = other as ListEventsForUserData;
    return events == otherTyped.events;
    
  }
  @override
  int get hashCode => events.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['events'] = events.map((e) => e.toJson()).toList();
    return json;
  }

  ListEventsForUserData({
    required this.events,
  });
}

