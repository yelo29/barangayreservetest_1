part of 'generated.dart';

class CreateNewsItemVariablesBuilder {
  String title;
  String content;
  Optional<String> _category = Optional.optional(nativeFromJson, nativeToJson);
  Optional<String> _imageUrl = Optional.optional(nativeFromJson, nativeToJson);

  final FirebaseDataConnect _dataConnect;  CreateNewsItemVariablesBuilder category(String? t) {
   _category.value = t;
   return this;
  }
  CreateNewsItemVariablesBuilder imageUrl(String? t) {
   _imageUrl.value = t;
   return this;
  }

  CreateNewsItemVariablesBuilder(this._dataConnect, {required  this.title,required  this.content,});
  Deserializer<CreateNewsItemData> dataDeserializer = (dynamic json)  => CreateNewsItemData.fromJson(jsonDecode(json));
  Serializer<CreateNewsItemVariables> varsSerializer = (CreateNewsItemVariables vars) => jsonEncode(vars.toJson());
  Future<OperationResult<CreateNewsItemData, CreateNewsItemVariables>> execute() {
    return ref().execute();
  }

  MutationRef<CreateNewsItemData, CreateNewsItemVariables> ref() {
    CreateNewsItemVariables vars= CreateNewsItemVariables(title: title,content: content,category: _category,imageUrl: _imageUrl,);
    return _dataConnect.mutation("CreateNewsItem", dataDeserializer, varsSerializer, vars);
  }
}

@immutable
class CreateNewsItemNewsItemInsert {
  final String id;
  CreateNewsItemNewsItemInsert.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateNewsItemNewsItemInsert otherTyped = other as CreateNewsItemNewsItemInsert;
    return id == otherTyped.id;
    
  }
  @override
  int get hashCode => id.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    return json;
  }

  CreateNewsItemNewsItemInsert({
    required this.id,
  });
}

@immutable
class CreateNewsItemData {
  final CreateNewsItemNewsItemInsert newsItem_insert;
  CreateNewsItemData.fromJson(dynamic json):
  
  newsItem_insert = CreateNewsItemNewsItemInsert.fromJson(json['newsItem_insert']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateNewsItemData otherTyped = other as CreateNewsItemData;
    return newsItem_insert == otherTyped.newsItem_insert;
    
  }
  @override
  int get hashCode => newsItem_insert.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['newsItem_insert'] = newsItem_insert.toJson();
    return json;
  }

  CreateNewsItemData({
    required this.newsItem_insert,
  });
}

@immutable
class CreateNewsItemVariables {
  final String title;
  final String content;
  late final Optional<String>category;
  late final Optional<String>imageUrl;
  @Deprecated('fromJson is deprecated for Variable classes as they are no longer required for deserialization.')
  CreateNewsItemVariables.fromJson(Map<String, dynamic> json):
  
  title = nativeFromJson<String>(json['title']),
  content = nativeFromJson<String>(json['content']) {
  
  
  
  
    category = Optional.optional(nativeFromJson, nativeToJson);
    category.value = json['category'] == null ? null : nativeFromJson<String>(json['category']);
  
  
    imageUrl = Optional.optional(nativeFromJson, nativeToJson);
    imageUrl.value = json['imageUrl'] == null ? null : nativeFromJson<String>(json['imageUrl']);
  
  }
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateNewsItemVariables otherTyped = other as CreateNewsItemVariables;
    return title == otherTyped.title && 
    content == otherTyped.content && 
    category == otherTyped.category && 
    imageUrl == otherTyped.imageUrl;
    
  }
  @override
  int get hashCode => Object.hashAll([title.hashCode, content.hashCode, category.hashCode, imageUrl.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['title'] = nativeToJson<String>(title);
    json['content'] = nativeToJson<String>(content);
    if(category.state == OptionalState.set) {
      json['category'] = category.toJson();
    }
    if(imageUrl.state == OptionalState.set) {
      json['imageUrl'] = imageUrl.toJson();
    }
    return json;
  }

  CreateNewsItemVariables({
    required this.title,
    required this.content,
    required this.category,
    required this.imageUrl,
  });
}

