# Technical Q&A Documentation

## 🔧 Authentication & Database Technical Details

---

## ❓ QUESTION 1: Authentication Methods Used

### **🔐 AUTHENTICATION SYSTEM OVERVIEW**

The Barangay Reserve System implements a comprehensive authentication system with multiple layers of security and session management.

---

### **📱 LOGIN SCREENS**

#### **🏠 Resident Authentication**
- **File**: `lib/screens/resident_login_screen.dart`
- **Purpose**: Resident user login and registration
- **Features**: Email/password authentication, registration form

#### **🏛️ Official Authentication**
- **File**: `lib/screens/official_login_screen.dart`
- **Purpose**: Official user login
- **Features**: Email/password authentication, role-based access

---

### **🔧 AUTHENTICATION SERVICES**

#### **🎯 Main Authentication Service**
- **File**: `lib/services/auth_api_service.dart`
- **Class**: `AuthApiService`
- **Pattern**: Singleton pattern
- **Purpose**: Centralized authentication management

#### **🌐 API Authentication Service**
- **File**: `lib/services/api_service.dart`
- **Class**: `ApiService`
- **Purpose**: HTTP API authentication and token management

---

### **🔑 AUTHENTICATION METHODS**

#### **📝 USER REGISTRATION**
```dart
// AuthApiService Methods
Future<Map<String, dynamic>> registerWithEmailAndPassword(
  String name, 
  String email, 
  String password, 
  {String role = 'resident'}
)

// ApiService Methods
Future<Map<String, dynamic>> register(
  String name, 
  String email, 
  String password, 
  {String role = 'resident'}
)
```

#### **🔑 USER LOGIN**
```dart
// AuthApiService Methods
Future<Map<String, dynamic>> signInWithEmailAndPassword(
  String email, 
  String password, 
  {String role = 'resident'}
)

// ApiService Methods
Future<Map<String, dynamic>> login(String email, String password)
```

#### **🚪 USER LOGOUT**
```dart
// AuthApiService Methods
Future<Map<String, dynamic>> signOut()

// ApiService Methods
Future<Map<String, dynamic>> logout()
```

---

### **🔄 SESSION MANAGEMENT**

#### **🎫 TOKEN MANAGEMENT**
```dart
// Token Storage
static Future<void> _saveToken(String token)
static Future<String?> _getToken()
static Future<void> _removeToken()

// Token Usage
static Future<Map<String, String>> getHeaders({bool includeAuth = true})
```

#### **👤 USER SESSION**
```dart
// Session Control
Future<void> initializeUser()
Future<Map<String, dynamic>?> restoreUserFromToken()
Future<Map<String, dynamic>?> ensureUserLoaded()
bool get isAuthenticated
Map<String, dynamic>? get currentUser
```

---

### **🛡️ SECURITY FEATURES**

#### **🚫 BAN VALIDATION**
```dart
// Ban Detection
static Future<void> checkAndHandleBanStatus()
static Future<void> _forceLogoutForBannedUser(String banReason)
```

#### **🔒 AUTHENTICATION HEADERS**
```dart
// HTTP Headers with Bearer Token
static Future<Map<String, String>> getHeaders() async {
  Map<String, String> headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  final token = await _getToken();
  if (token != null) {
    headers['Authorization'] = 'Bearer $token';
  }

  return headers;
}
```

---

### **🔄 AUTHENTICATION FLOW**

```
USER LOGIN
    ↓
EMAIL/PASSWORD VALIDATION
    ↓
API CALL TO /api/auth/login
    ↓
RECEIVE JWT-LIKE TOKEN
    ↓
SAVE TOKEN TO SHAREDPREFERENCES
    ↓
SET CURRENT USER DATA
    ↓
NAVIGATE TO DASHBOARD
    ↓
AUTOMATIC TOKEN INCLUSION IN API CALLS
    ↓
BAN STATUS VALIDATION
    ↓
LOGOUT → TOKEN REMOVAL
```

---

## ❓ QUESTION 2: SQLite Language & Composition

### **💾 SQLITE TECHNICAL SPECIFICATIONS**

SQLite is a self-contained, serverless, zero-configuration SQL database engine written in C programming language.

---

### **🔧 PROGRAMMING LANGUAGE**

#### **📦 CORE LANGUAGE**
- **Primary Language**: **C Programming Language**
- **Standard**: ANSI C (C89/C99 compliant)
- **Compiler**: Any standard C compiler
- **Portability**: Cross-platform compatible
- **License**: Public domain

#### **🏗️ ARCHITECTURE**
```
┌─────────────────────────────────────────┐
│           SQLITE ARCHITECTURE        │
├─────────────────────────────────────────┤
│  C Library (sqlite3.c)             │
│  ├── SQL Parser                    │
│  ├── Code Generator                │
│  ├── Virtual Machine               │
│  ├── B-Tree Storage               │
│  └── Pager (File I/O)            │
├─────────────────────────────────────────┤
│  Database File (.db)               │
│  ├── Schema Table                  │
│  ├── Data Tables                  │
│  ├── Indexes                      │
│  └── Journal Files                 │
└─────────────────────────────────────────┘
```

---

### **🗄️ TECHNICAL COMPOSITION**

#### **📦 CORE COMPONENTS**
- **SQLite Library**: Single C library file (`sqlite3.c`)
- **Header File**: Interface definitions (`sqlite3.h`)
- **Database Engine**: Transactional SQL database engine
- **Virtual Machine**: SQL bytecode interpreter
- **B-Tree Storage**: Efficient data organization
- **Pager Module**: File I/O and caching

#### **💾 STORAGE FORMAT**
- **File Format**: Proprietary binary format
- **Database File**: `.db` extension
- **Page Size**: Default 4096 bytes (configurable)
- **Journaling**: Write-Ahead Logging (WAL)
- **Schema Storage**: `sqlite_master` table

---

### **📊 DATABASE FILE STRUCTURE**

#### **🗃️ FILE ORGANIZATION**
```
┌─────────────────────────────────────────┐
│         DATABASE FILE (.db)          │
├─────────────────────────────────────────┤
│  Header (100 bytes)                │
│  ├── Magic Number                  │
│  ├── Page Size                     │
│  ├── File Format Version            │
│  └── Schema Cookie                 │
├─────────────────────────────────────────┤
│  B-Tree Pages                     │
│  ├── Table B-Trees                │
│  ├── Index B-Trees                │
│  └── Overflow Pages               │
├─────────────────────────────────────────┤
│  Schema Layer                     │
│  ├── sqlite_master Table            │
│  ├── Table Definitions            │
│  └── Index Definitions            │
└─────────────────────────────────────────┘
```

---

### **⚙️ KEY CHARACTERISTICS**

#### **💻 LANGUAGE FEATURES**
- **Compiled**: Pre-compiled C library
- **Embedded**: No separate server process
- **Self-contained**: Single database file
- **Zero-configuration**: No setup required
- **Serverless**: Direct file access

#### **🗄️ DATABASE ENGINE**
- **ACID Compliant**: Atomic, Consistent, Isolated, Durable
- **SQL-92**: Most SQL-92 standards supported
- **Dynamic Typing**: Flexible data types
- **B-Tree Storage**: Efficient data organization
- **Referential Integrity**: Foreign key constraints

---

### **🔧 IMPLEMENTATION IN BARANGAY SYSTEM**

#### **📱 FLUTTER INTEGRATION**
- **Package**: `sqflite` (Flutter SQLite plugin)
- **Platform**: Native Android/iOS SQLite libraries
- **API**: Dart wrapper around C library
- **Connection**: Direct file access

#### **🖥️ FLASK BACKEND**
- **Library**: `sqlite3` Python module
- **Interface**: Python wrapper around C library
- **Connection**: Direct file access to `.db`
- **Operations**: SQL queries and transactions

#### **📊 OUR DATABASE**
- **File**: `server/barangay.db`
- **Size**: Typically 1-10MB
- **Tables**: 5 main tables
- **Indexes**: Optimized for queries
- **Foreign Keys**: Enforced relationships

---

### **📈 PERFORMANCE CHARACTERISTICS**

#### **⚡ SPEED & EFFICIENCY**
- **Read Operations**: Very fast (in-memory caching)
- **Write Operations**: Fast (transactional)
- **File Size**: Compact (efficient storage)
- **Memory**: Low footprint
- **Concurrency**: Multiple readers, single writer

#### **🛡️ RELIABILITY**
- **Atomic Operations**: No corruption
- **Journaling**: Recovery from crashes
- **Type Safety**: Dynamic but validated
- **ACID Properties**: Data integrity guaranteed
- **Durability**: Persistent storage

---

### **🎯 SQL CAPABILITIES**

#### **📋 SUPPORTED SQL FEATURES**
- **DDL**: CREATE, ALTER, DROP tables
- **DML**: INSERT, UPDATE, DELETE, SELECT
- **DQL**: Complex SELECT with JOINs
- **Indexes**: CREATE INDEX, DROP INDEX
- **Views**: CREATE VIEW, DROP VIEW
- **Triggers**: CREATE TRIGGER, DROP TRIGGER
- **Transactions**: BEGIN, COMMIT, ROLLBACK

#### **🔍 DATA TYPES**
- **NULL**: NULL values
- **INTEGER**: Signed integers
- **REAL**: Floating point numbers
- **TEXT**: Text strings
- **BLOB**: Binary data

---

## 🎯 SUMMARY

### **🔐 AUTHENTICATION SYSTEM**
- **Multi-layer**: Login screens + services + API
- **Token-based**: JWT-like Bearer tokens
- **Session management**: SharedPreferences persistence
- **Security**: Ban validation and protection
- **Role-based**: Resident vs Official access

### **💾 SQLITE DATABASE**
- **Language**: C programming language
- **Architecture**: Embedded, serverless, file-based
- **Storage**: Single `.db` file with B-Tree structure
- **Performance**: Fast, reliable, ACID compliant
- **Integration**: Native Flutter/Python wrappers

This technical foundation provides a robust, secure, and efficient system for barangay facility reservation management.
