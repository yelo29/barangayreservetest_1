part of 'generated.dart';

class UpdateUserProfileVariablesBuilder {
  Optional<String> _bio = Optional.optional(nativeFromJson, nativeToJson);
  Optional<String> _location = Optional.optional(nativeFromJson, nativeToJson);
  Optional<String> _photoUrl = Optional.optional(nativeFromJson, nativeToJson);
  Optional<String> _displayName = Optional.optional(nativeFromJson, nativeToJson);

  final FirebaseDataConnect _dataConnect;
  UpdateUserProfileVariablesBuilder bio(String? t) {
   _bio.value = t;
   return this;
  }
  UpdateUserProfileVariablesBuilder location(String? t) {
   _location.value = t;
   return this;
  }
  UpdateUserProfileVariablesBuilder photoUrl(String? t) {
   _photoUrl.value = t;
   return this;
  }
  UpdateUserProfileVariablesBuilder displayName(String? t) {
   _displayName.value = t;
   return this;
  }

  UpdateUserProfileVariablesBuilder(this._dataConnect, );
  Deserializer<UpdateUserProfileData> dataDeserializer = (dynamic json)  => UpdateUserProfileData.fromJson(jsonDecode(json));
  Serializer<UpdateUserProfileVariables> varsSerializer = (UpdateUserProfileVariables vars) => jsonEncode(vars.toJson());
  Future<OperationResult<UpdateUserProfileData, UpdateUserProfileVariables>> execute() {
    return ref().execute();
  }

  MutationRef<UpdateUserProfileData, UpdateUserProfileVariables> ref() {
    UpdateUserProfileVariables vars= UpdateUserProfileVariables(bio: _bio,location: _location,photoUrl: _photoUrl,displayName: _displayName,);
    return _dataConnect.mutation("UpdateUserProfile", dataDeserializer, varsSerializer, vars);
  }
}

@immutable
class UpdateUserProfileUserUpdate {
  final String id;
  UpdateUserProfileUserUpdate.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final UpdateUserProfileUserUpdate otherTyped = other as UpdateUserProfileUserUpdate;
    return id == otherTyped.id;
    
  }
  @override
  int get hashCode => id.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    return json;
  }

  UpdateUserProfileUserUpdate({
    required this.id,
  });
}

@immutable
class UpdateUserProfileData {
  final UpdateUserProfileUserUpdate? user_update;
  UpdateUserProfileData.fromJson(dynamic json):
  
  user_update = json['user_update'] == null ? null : UpdateUserProfileUserUpdate.fromJson(json['user_update']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final UpdateUserProfileData otherTyped = other as UpdateUserProfileData;
    return user_update == otherTyped.user_update;
    
  }
  @override
  int get hashCode => user_update.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if (user_update != null) {
      json['user_update'] = user_update!.toJson();
    }
    return json;
  }

  UpdateUserProfileData({
    this.user_update,
  });
}

@immutable
class UpdateUserProfileVariables {
  late final Optional<String>bio;
  late final Optional<String>location;
  late final Optional<String>photoUrl;
  late final Optional<String>displayName;
  @Deprecated('fromJson is deprecated for Variable classes as they are no longer required for deserialization.')
  UpdateUserProfileVariables.fromJson(Map<String, dynamic> json) {
  
  
    bio = Optional.optional(nativeFromJson, nativeToJson);
    bio.value = json['bio'] == null ? null : nativeFromJson<String>(json['bio']);
  
  
    location = Optional.optional(nativeFromJson, nativeToJson);
    location.value = json['location'] == null ? null : nativeFromJson<String>(json['location']);
  
  
    photoUrl = Optional.optional(nativeFromJson, nativeToJson);
    photoUrl.value = json['photoUrl'] == null ? null : nativeFromJson<String>(json['photoUrl']);
  
  
    displayName = Optional.optional(nativeFromJson, nativeToJson);
    displayName.value = json['displayName'] == null ? null : nativeFromJson<String>(json['displayName']);
  
  }
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final UpdateUserProfileVariables otherTyped = other as UpdateUserProfileVariables;
    return bio == otherTyped.bio && 
    location == otherTyped.location && 
    photoUrl == otherTyped.photoUrl && 
    displayName == otherTyped.displayName;
    
  }
  @override
  int get hashCode => Object.hashAll([bio.hashCode, location.hashCode, photoUrl.hashCode, displayName.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if(bio.state == OptionalState.set) {
      json['bio'] = bio.toJson();
    }
    if(location.state == OptionalState.set) {
      json['location'] = location.toJson();
    }
    if(photoUrl.state == OptionalState.set) {
      json['photoUrl'] = photoUrl.toJson();
    }
    if(displayName.state == OptionalState.set) {
      json['displayName'] = displayName.toJson();
    }
    return json;
  }

  UpdateUserProfileVariables({
    required this.bio,
    required this.location,
    required this.photoUrl,
    required this.displayName,
  });
}

