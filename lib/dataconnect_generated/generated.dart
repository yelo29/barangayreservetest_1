library dataconnect_generated;
import 'package:firebase_data_connect/firebase_data_connect.dart';
import 'package:flutter/foundation.dart';
import 'dart:convert';

part 'create_news_item.dart';

part 'list_businesses_by_category.dart';

part 'update_user_profile.dart';

part 'list_events_for_user.dart';







class ExampleConnector {
  
  
  CreateNewsItemVariablesBuilder createNewsItem ({required String title, required String content, }) {
    return CreateNewsItemVariablesBuilder(dataConnect, title: title,content: content,);
  }
  
  
  ListBusinessesByCategoryVariablesBuilder listBusinessesByCategory ({required String category, }) {
    return ListBusinessesByCategoryVariablesBuilder(dataConnect, category: category,);
  }
  
  
  UpdateUserProfileVariablesBuilder updateUserProfile () {
    return UpdateUserProfileVariablesBuilder(dataConnect, );
  }
  
  
  ListEventsForUserVariablesBuilder listEventsForUser () {
    return ListEventsForUserVariablesBuilder(dataConnect, );
  }
  

  static ConnectorConfig connectorConfig = ConnectorConfig(
    'us-east4',
    'example',
    'barangayreservetest1',
  );

  ExampleConnector({required this.dataConnect});
  static ExampleConnector get instance {
    return ExampleConnector(
        dataConnect: FirebaseDataConnect.instanceFor(
            connectorConfig: connectorConfig,
            sdkType: CallerSDKType.generated));
  }

  FirebaseDataConnect dataConnect;
}
