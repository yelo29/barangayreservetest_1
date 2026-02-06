import { ConnectorConfig, DataConnect, OperationOptions, ExecuteOperationResponse } from 'firebase-admin/data-connect';

export const connectorConfig: ConnectorConfig;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;


export interface Business_Key {
  id: UUIDString;
  __typename?: 'Business_Key';
}

export interface CreateNewsItemData {
  newsItem_insert: {
    id: UUIDString;
  };
}

export interface CreateNewsItemVariables {
  title: string;
  content: string;
  category?: string | null;
  imageUrl?: string | null;
}

export interface Event_Key {
  id: UUIDString;
  __typename?: 'Event_Key';
}

export interface ForumPost_Key {
  id: UUIDString;
  __typename?: 'ForumPost_Key';
}

export interface ListBusinessesByCategoryData {
  businesses: ({
    id: UUIDString;
    name: string;
    address: string;
    contactNumber: string;
    operatingHours?: string | null;
    website?: string | null;
    description?: string | null;
    imageUrl?: string | null;
  } & Business_Key)[];
}

export interface ListBusinessesByCategoryVariables {
  category: string;
}

export interface ListEventsForUserData {
  events: ({
    id: UUIDString;
    name: string;
    description: string;
    location: string;
    eventDate: TimestampString;
    category?: string | null;
    contactInfo?: string | null;
    imageUrl?: string | null;
  } & Event_Key)[];
}

export interface NewsItem_Key {
  id: UUIDString;
  __typename?: 'NewsItem_Key';
}

export interface UpdateUserProfileData {
  user_update?: {
    id: UUIDString;
  };
}

export interface UpdateUserProfileVariables {
  bio?: string | null;
  location?: string | null;
  photoUrl?: string | null;
  displayName?: string | null;
}

export interface User_Key {
  id: UUIDString;
  __typename?: 'User_Key';
}

/** Generated Node Admin SDK operation action function for the 'CreateNewsItem' Mutation. Allow users to execute without passing in DataConnect. */
export function createNewsItem(dc: DataConnect, vars: CreateNewsItemVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<CreateNewsItemData>>;
/** Generated Node Admin SDK operation action function for the 'CreateNewsItem' Mutation. Allow users to pass in custom DataConnect instances. */
export function createNewsItem(vars: CreateNewsItemVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<CreateNewsItemData>>;

/** Generated Node Admin SDK operation action function for the 'ListBusinessesByCategory' Query. Allow users to execute without passing in DataConnect. */
export function listBusinessesByCategory(dc: DataConnect, vars: ListBusinessesByCategoryVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<ListBusinessesByCategoryData>>;
/** Generated Node Admin SDK operation action function for the 'ListBusinessesByCategory' Query. Allow users to pass in custom DataConnect instances. */
export function listBusinessesByCategory(vars: ListBusinessesByCategoryVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<ListBusinessesByCategoryData>>;

/** Generated Node Admin SDK operation action function for the 'UpdateUserProfile' Mutation. Allow users to execute without passing in DataConnect. */
export function updateUserProfile(dc: DataConnect, vars?: UpdateUserProfileVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<UpdateUserProfileData>>;
/** Generated Node Admin SDK operation action function for the 'UpdateUserProfile' Mutation. Allow users to pass in custom DataConnect instances. */
export function updateUserProfile(vars?: UpdateUserProfileVariables, options?: OperationOptions): Promise<ExecuteOperationResponse<UpdateUserProfileData>>;

/** Generated Node Admin SDK operation action function for the 'ListEventsForUser' Query. Allow users to execute without passing in DataConnect. */
export function listEventsForUser(dc: DataConnect, options?: OperationOptions): Promise<ExecuteOperationResponse<ListEventsForUserData>>;
/** Generated Node Admin SDK operation action function for the 'ListEventsForUser' Query. Allow users to pass in custom DataConnect instances. */
export function listEventsForUser(options?: OperationOptions): Promise<ExecuteOperationResponse<ListEventsForUserData>>;

