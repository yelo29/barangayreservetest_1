part of 'generated.dart';

class ListBusinessesByCategoryVariablesBuilder {
  String category;

  final FirebaseDataConnect _dataConnect;
  ListBusinessesByCategoryVariablesBuilder(this._dataConnect, {required  this.category,});
  Deserializer<ListBusinessesByCategoryData> dataDeserializer = (dynamic json)  => ListBusinessesByCategoryData.fromJson(jsonDecode(json));
  Serializer<ListBusinessesByCategoryVariables> varsSerializer = (ListBusinessesByCategoryVariables vars) => jsonEncode(vars.toJson());
  Future<QueryResult<ListBusinessesByCategoryData, ListBusinessesByCategoryVariables>> execute() {
    return ref().execute();
  }

  QueryRef<ListBusinessesByCategoryData, ListBusinessesByCategoryVariables> ref() {
    ListBusinessesByCategoryVariables vars= ListBusinessesByCategoryVariables(category: category,);
    return _dataConnect.query("ListBusinessesByCategory", dataDeserializer, varsSerializer, vars);
  }
}

@immutable
class ListBusinessesByCategoryBusinesses {
  final String id;
  final String name;
  final String address;
  final String contactNumber;
  final String? operatingHours;
  final String? website;
  final String? description;
  final String? imageUrl;
  ListBusinessesByCategoryBusinesses.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']),
  name = nativeFromJson<String>(json['name']),
  address = nativeFromJson<String>(json['address']),
  contactNumber = nativeFromJson<String>(json['contactNumber']),
  operatingHours = json['operatingHours'] == null ? null : nativeFromJson<String>(json['operatingHours']),
  website = json['website'] == null ? null : nativeFromJson<String>(json['website']),
  description = json['description'] == null ? null : nativeFromJson<String>(json['description']),
  imageUrl = json['imageUrl'] == null ? null : nativeFromJson<String>(json['imageUrl']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final ListBusinessesByCategoryBusinesses otherTyped = other as ListBusinessesByCategoryBusinesses;
    return id == otherTyped.id && 
    name == otherTyped.name && 
    address == otherTyped.address && 
    contactNumber == otherTyped.contactNumber && 
    operatingHours == otherTyped.operatingHours && 
    website == otherTyped.website && 
    description == otherTyped.description && 
    imageUrl == otherTyped.imageUrl;
    
  }
  @override
  int get hashCode => Object.hashAll([id.hashCode, name.hashCode, address.hashCode, contactNumber.hashCode, operatingHours.hashCode, website.hashCode, description.hashCode, imageUrl.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    json['name'] = nativeToJson<String>(name);
    json['address'] = nativeToJson<String>(address);
    json['contactNumber'] = nativeToJson<String>(contactNumber);
    if (operatingHours != null) {
      json['operatingHours'] = nativeToJson<String?>(operatingHours);
    }
    if (website != null) {
      json['website'] = nativeToJson<String?>(website);
    }
    if (description != null) {
      json['description'] = nativeToJson<String?>(description);
    }
    if (imageUrl != null) {
      json['imageUrl'] = nativeToJson<String?>(imageUrl);
    }
    return json;
  }

  ListBusinessesByCategoryBusinesses({
    required this.id,
    required this.name,
    required this.address,
    required this.contactNumber,
    this.operatingHours,
    this.website,
    this.description,
    this.imageUrl,
  });
}

@immutable
class ListBusinessesByCategoryData {
  final List<ListBusinessesByCategoryBusinesses> businesses;
  ListBusinessesByCategoryData.fromJson(dynamic json):
  
  businesses = (json['businesses'] as List<dynamic>)
        .map((e) => ListBusinessesByCategoryBusinesses.fromJson(e))
        .toList();
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final ListBusinessesByCategoryData otherTyped = other as ListBusinessesByCategoryData;
    return businesses == otherTyped.businesses;
    
  }
  @override
  int get hashCode => businesses.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['businesses'] = businesses.map((e) => e.toJson()).toList();
    return json;
  }

  ListBusinessesByCategoryData({
    required this.businesses,
  });
}

@immutable
class ListBusinessesByCategoryVariables {
  final String category;
  @Deprecated('fromJson is deprecated for Variable classes as they are no longer required for deserialization.')
  ListBusinessesByCategoryVariables.fromJson(Map<String, dynamic> json):
  
  category = nativeFromJson<String>(json['category']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final ListBusinessesByCategoryVariables otherTyped = other as ListBusinessesByCategoryVariables;
    return category == otherTyped.category;
    
  }
  @override
  int get hashCode => category.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['category'] = nativeToJson<String>(category);
    return json;
  }

  ListBusinessesByCategoryVariables({
    required this.category,
  });
}

