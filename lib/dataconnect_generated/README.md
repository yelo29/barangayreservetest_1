# dataconnect_generated SDK

## Installation
```sh
flutter pub get firebase_data_connect
flutterfire configure
```
For more information, see [Flutter for Firebase installation documentation](https://firebase.google.com/docs/data-connect/flutter-sdk#use-core).

## Data Connect instance
Each connector creates a static class, with an instance of the `DataConnect` class that can be used to connect to your Data Connect backend and call operations.

### Connecting to the emulator

```dart
String host = 'localhost'; // or your host name
int port = 9399; // or your port number
ExampleConnector.instance.dataConnect.useDataConnectEmulator(host, port);
```

You can also call queries and mutations by using the connector class.
## Queries

### ListBusinessesByCategory
#### Required Arguments
```dart
String category = ...;
ExampleConnector.instance.listBusinessesByCategory(
  category: category,
).execute();
```



#### Return Type
`execute()` returns a `QueryResult<ListBusinessesByCategoryData, ListBusinessesByCategoryVariables>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

/// Result of a query request. Created to hold extra variables in the future.
class QueryResult<Data, Variables> extends OperationResult<Data, Variables> {
  QueryResult(super.dataConnect, super.data, super.ref);
}

final result = await ExampleConnector.instance.listBusinessesByCategory(
  category: category,
);
ListBusinessesByCategoryData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
String category = ...;

final ref = ExampleConnector.instance.listBusinessesByCategory(
  category: category,
).ref();
ref.execute();

ref.subscribe(...);
```


### ListEventsForUser
#### Required Arguments
```dart
// No required arguments
ExampleConnector.instance.listEventsForUser().execute();
```



#### Return Type
`execute()` returns a `QueryResult<ListEventsForUserData, void>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

/// Result of a query request. Created to hold extra variables in the future.
class QueryResult<Data, Variables> extends OperationResult<Data, Variables> {
  QueryResult(super.dataConnect, super.data, super.ref);
}

final result = await ExampleConnector.instance.listEventsForUser();
ListEventsForUserData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
final ref = ExampleConnector.instance.listEventsForUser().ref();
ref.execute();

ref.subscribe(...);
```

## Mutations

### CreateNewsItem
#### Required Arguments
```dart
String title = ...;
String content = ...;
ExampleConnector.instance.createNewsItem(
  title: title,
  content: content,
).execute();
```

#### Optional Arguments
We return a builder for each query. For CreateNewsItem, we created `CreateNewsItemBuilder`. For queries and mutations with optional parameters, we return a builder class.
The builder pattern allows Data Connect to distinguish between fields that haven't been set and fields that have been set to null. A field can be set by calling its respective setter method like below:
```dart
class CreateNewsItemVariablesBuilder {
  ...
   CreateNewsItemVariablesBuilder category(String? t) {
   _category.value = t;
   return this;
  }
  CreateNewsItemVariablesBuilder imageUrl(String? t) {
   _imageUrl.value = t;
   return this;
  }

  ...
}
ExampleConnector.instance.createNewsItem(
  title: title,
  content: content,
)
.category(category)
.imageUrl(imageUrl)
.execute();
```

#### Return Type
`execute()` returns a `OperationResult<CreateNewsItemData, CreateNewsItemVariables>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

final result = await ExampleConnector.instance.createNewsItem(
  title: title,
  content: content,
);
CreateNewsItemData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
String title = ...;
String content = ...;

final ref = ExampleConnector.instance.createNewsItem(
  title: title,
  content: content,
).ref();
ref.execute();
```


### UpdateUserProfile
#### Required Arguments
```dart
// No required arguments
ExampleConnector.instance.updateUserProfile().execute();
```

#### Optional Arguments
We return a builder for each query. For UpdateUserProfile, we created `UpdateUserProfileBuilder`. For queries and mutations with optional parameters, we return a builder class.
The builder pattern allows Data Connect to distinguish between fields that haven't been set and fields that have been set to null. A field can be set by calling its respective setter method like below:
```dart
class UpdateUserProfileVariablesBuilder {
  ...
 
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

  ...
}
ExampleConnector.instance.updateUserProfile()
.bio(bio)
.location(location)
.photoUrl(photoUrl)
.displayName(displayName)
.execute();
```

#### Return Type
`execute()` returns a `OperationResult<UpdateUserProfileData, UpdateUserProfileVariables>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

final result = await ExampleConnector.instance.updateUserProfile();
UpdateUserProfileData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
final ref = ExampleConnector.instance.updateUserProfile().ref();
ref.execute();
```

