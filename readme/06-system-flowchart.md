# System Flowchart Documentation

## 🔄 Complete System Architecture Flow

---

## 🎯 Overall System Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    BARANGAY RESERVE SYSTEM                           │
│                    (Flutter + Flask + SQLite)                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     USER ACCESS POINT                                │
│                  (Selection Screen)                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                    ┌─────────┴─────────┐
                    │                   │
                ┌───▼───┐         ┌───▼───┐
                │           │         │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │
    RESIDENT     OFFICIAL    DATABASE    API         BAN         SECURITY
    WORKFLOW     WORKFLOW     STORAGE     LAYER       SYSTEM      FEATURES
```

---

## 👥 User Role Selection Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    SELECTION SCREEN                                │
│                  (Role Entry Point)                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│           │ │           │ │           │ │           │ │           │ │           │
│  I'M A    │  I'M A     │  CHECK     │  NAVIGATE  │  LOAD      │  DISPLAY    │  ROLE      │
│  RESIDENT  │  BARANGAY   │  SESSION    │  TO DASH   │  DASHBOARD  │  SPECIFIC   │  FEATURES   │
│           │  OFFICIAL    │             │  BOARD      │             │  FEATURES   │             │
└───▼───┘ └───▼───┘ └───▼───┘ └───▼───┘ └───▼───┘ └───▼───┘ └───▼───┘
    │           │             │             │             │             │             │
    ▼           ▼             ▼             ▼             ▼             ▼
┌───▼───┐ ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│           │ │           │   │           │   │           │   │           │
│ RESIDENT   │ OFFICIAL    │  LOGIN      │  BOOKING    │  APPROVAL   │  USER       │
│ LOGIN     │ LOGIN      │  SCREEN     │  FORM       │  WORKFLOW   │  MANAGEMENT  │
└───▼───┘ └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
```

---

## 🗄️ Database Architecture Flow

```
                    ┌─────────────────────────────────────────────┐
                    │          SQLITE DATABASE              │
                    │         (barangay.db)              │
                    │                                     │
                    │         ┌─────────────────┐         │
                    │         │                 │         │
                    │    ┌────▼────┐   ┌────▼────┐   │
                    │    │           │   │           │   │
                    │ ┌──▼───┐   ┌──▼───┐   ┌──▼───┐   │
                    │ │           │   │           │   │           │   │
                ┌───▼───┐   ┌──▼───┐   ┌──▼───┐   ┌──▼───┐   │
                │           │   │           │   │           │   │           │   │
            ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   │
            │                 │   │                 │   │                 │   │           │
        ┌───▼───┐         ┌───▼───┐         ┌───▼───┐         ┌───▼───┐         │
        │           │         │           │         │           │         │           │         │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
    │  USERS    │ FACILITIES  │ BOOKINGS   │ VERIFI-   │ TIME-     │ INDEXES    │ RELATIONS- │
    │  TABLE    │  TABLE     │  TABLE     │ CATION    │ SLOTS     │  FOR       │  HIPS      │
    │           │            │            │ REQUESTS   │ TABLE     │  PERFOR-   │            │            │
    │           │            │            │ TABLE     │            │  MANCE     │            │            │
    └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
        │           │            │            │            │            │            │            │
        ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ USER        │ FACILITY     │ BOOKING      │ VERIFICATION │ AVAILABILITY │ FOREIGN KEY   │ BAN         │ AUDIT       │
│ ACCOUNTS    │ MANAGEMENT   │ TRACKING     │ WORKFLOW     │ MANAGEMENT   │ CONSTRAINTS  │ SYSTEM       │ TRAIL       │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 🔄 Resident User Workflow Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    RESIDENT WORKFLOW                                │
│                  (Complete User Journey)                             │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
│  LOGIN     │  DASHBOARD   │  BROWSE     │  SELECT     │  BOOK       │  UPLOAD     │  TRACK      │  MANAGE     │
│  SCREEN    │  DISPLAY    │  FACILITIES  │  TIME SLOT  │  FACILITY   │  RECEIPT   │  BOOKING    │  PROFILE     │
└───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
    │           │            │            │            │            │            │            │
    ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ AUTHEN-    │ QUICK       │ CALENDAR    │ PAYMENT     │ BOOKING     │ STATUS      │ VERIFI-     │ ACCOUNT     │
│ TICATION   │ ACCESS       │ INTERFACE   │ INTEGRATION │ CONFIRMA-   │ NOTIFI-     │ CATION      │ SETTINGS    │
│            │             │             │             │ TION        │ CATIONS    │ WORKFLOW    │             │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 🏛️ Official User Workflow Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    OFFICIAL WORKFLOW                                 │
│                  (Administrative Journey)                             │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
│  LOGIN     │  DASHBOARD   │  REVIEW      │  APPROVE/   │  MANAGE     │  VERIFY      │  CONFIGURE   │  GENERATE    │
│  SCREEN    │  OVERVIEW   │  REQUESTS    │  REJECT     │  FACILITIES  │  RESIDENTS   │  SYSTEM      │  REPORTS     │
└───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
    │           │            │            │            │            │            │            │
    ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ SESSION     │ STATISTICS   │ BOOKING     │ DECISION     │ FACILITY    │ USER        │ SYSTEM      │ ANALYTICS   │
│ MANAGEMENT  │ DISPLAY     │ MANAGEMENT   │ MAKING      │ MANAGEMENT  │ MANAGEMENT  │ SETTINGS    │ & REPORTING │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 🔐 Security & Ban System Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY SYSTEM                                     │
│                  (Ban Validation & Protection)                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
│  USER      │  BAN        │  BLOCK       │  SHOW       │  LOGOUT     │  UPDATE     │  NOTIFY     │  AUDIT       │
│  LOGIN     │  VALIDATION  │  BOOKING     │  BAN        │  USER       │  DATABASE   │  OFFICIALS   │  TRAIL       │
│  CHECK     │  CHECK      │  ATTEMPTS    │  DIALOG      │  SESSION    │  RECORD     │  OF ACTION   │             │
└───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
    │           │            │            │            │            │            │            │
    ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ REAL-TIME  │ SERVER-SIDE  │ CLIENT-SIDE  │ USER        │ SESSION     │ DATABASE    │ NOTIFI-     │ LOGGING     │
│ PROTECTION │ PROTECTION  │ PROTECTION  │ EXPERIENCE  │ SECURITY    │ INTEGRITY  │ CATION     │ SYSTEM      │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 🌐 API Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    API LAYER                                        │
│                  (HTTP Communication)                             │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
│  FLUTTER   │  HTTP      │  FLASK      │  SQLITE     │  JSON       │  BEARER     │  ERROR      │  RESPONSE    │
│  CLIENT    │  REQUESTS   │  SERVER     │  DATABASE   │  PARSING   │  TOKEN      │  HANDLING   │  HANDLING   │
└───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
    │           │            │            │            │            │            │            │
    ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ REQUEST    │  ROUTE      │  BUSINESS   │  QUERY      │  AUTHEN-   │  VALIDATION  │  STATUS      │  DATA        │
│  BUILDING  │  HANDLING   │  LOGIC      │  EXECUTION  │ TICATION   │             │  CODES       │  TRANSFORM   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    DATA FLOW                                        │
│                  (Information Architecture)                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │                 │
                ┌───▼─────┐     ┌───▼─────┐
                │           │     │           │
            ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
            │           │   │           │   │           │
        ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
        │           │   │           │   │           │   │           │   │           │
    ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
    │           │   │           │   │           │   │           │   │           │   │           │
│  USER      │  BOOKING    │  FACILITY   │  VERIFI-    │  PAYMENT    │  NOTIFI-    │  REPORT      │  BACKUP      │
│  INPUT     │  DATA       │  DATA       │  CATION    │  DATA       │  CATION    │  GENERATION  │  & RECOVERY │
└───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘   └───▼───┘
    │           │            │            │            │            │            │            │
    ▼           ▼            ▼            ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │             │             │             │             │             │             │             │
│ FORM       │  API CALLS  │  DATABASE   │  DOCUMENT   │  RECEIPT    │  EMAIL/SMS  │  STATISTICS  │  AUTOMATIC   │
│  VALIDATION │             │  QUERIES    │  STORAGE    │  UPLOAD     │  NOTIFI-    │  CALCULATION │  BACKUPS     │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 🎯 Complete System Integration

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           COMPLETE BARANGAY RESERVE SYSTEM                          │
│                     (All Components Working Together)                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                          ┌─────────────────────┐
                          │                     │
                      ┌───▼─────────┐     ┌───▼─────────┐
                      │                 │     │                 │
                  ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐
                  │                 │     │                 │     │                 │     │
              ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐
              │                 │     │                 │     │                 │     │                 │     │
          ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐     ┌───▼───┐
          │                 │     │                 │     │                 │     │                 │     │                 │     │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │                 │     │                 │     │                 │     │                 │     │                 │     │                 │
┌───▼───┐ │  FLUTTER   │  FLASK      │  SQLITE     │  BAN        │  ROLE       │  BOOKING    │  VERIFI-    │  PAYMENT    │  REPORTING   │  NOTIFI-    │
│  USERS   │  FRONTEND   │  BACKEND    │  DATABASE    │  SYSTEM     │  MANAGEMENT │  SYSTEM     │  CATION    │  SYSTEM     │  SYSTEM     │  CATION    │
└───▼───┘ │  (MOBILE)   │  (SERVER)   │  (STORAGE)   │  (SECURITY) │  (ACCESS)   │  (SLOTS)   │  (DOCS)    │  (ANALYTICS)│  (ALERTS)   │
    │        │             │             │             │             │             │             │             │             │             │
    ▼        ▼             ▼             ▼             ▼             ▼             ▼             ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│              │              │              │              │              │              │              │              │              │              │              │
│   MOBILE     │    WEB       │   DATABASE    │   SECURITY    │   USER        │   RESOURCE    │   DOCUMENT    │   FINANCIAL   │   ANALYTICAL   │   COMMUNI-    │
│   APPS       │   SERVICES    │   SERVICES    │   SERVICES    │   SERVICES    │   MANAGEMENT  │   MANAGEMENT  │   MANAGEMENT  │   SERVICES    │   CATION     │
│  (ANDROID/   │  (FLASK)     │  (SQLITE)    │  (BAN/      │  (LOGIN/     │  (TIME SLOTS)│  (VERIFI-    │  (RECEIPTS)  │  (REPORTS)   │  (EMAIL/SMS)  │
│   IOS)       │              │              │  AUTH)       │  SESSION)    │              │  CATION)     │              │              │              │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

---

## 🎨 Visual Legend

### **SHAPES MEANING**:
- **RECTANGLE (┌─┐)**: Process or system component
- **CYLINDER (│)**: Database or storage system
- **ARROWS (▼/│)**: Data flow and process direction
- **DIAMOND (◆)**: Decision point or validation
- **CIRCLE (○)**: Start/end point or state

### **COLOR CODING**:
- **BLUE**: User interface components
- **GREEN**: Database and storage
- **RED**: Security and validation
- **ORANGE**: Processing and business logic
- **PURPLE**: Communication and APIs
- **GRAY**: Integration and system flow

### **FLOW DIRECTION**:
- **VERTICAL (│)**: Sequential process flow
- **HORIZONTAL (─)**: Parallel processes or alternatives
- **DOWNWARD (▼)**: Process progression
- **ACROSS (→)**: Data movement or navigation

---

## 🚀 Implementation Notes

### **KEY INTEGRATION POINTS**:
1. **Selection Screen**: Role-based routing to appropriate workflows
2. **Authentication**: Token-based session management across all components
3. **Database**: Centralized SQLite storage with referential integrity
4. **API Layer**: RESTful communication between frontend and backend
5. **Security**: Multi-layer protection (client + server validation)

### **SCALABILITY CONSIDERATIONS**:
- **Database**: SQLite with proper indexing for performance
- **API**: Stateless design for horizontal scaling
- **Frontend**: Modular component architecture
- **Security**: Role-based access control system

### **MAINTENANCE FEATURES**:
- **Audit Trail**: Complete logging of all user actions
- **Data Integrity**: Foreign key constraints and validation
- **Backup Strategy**: SQLite file backup and recovery
- **Error Handling**: Graceful failure management and user feedback

This flowchart provides a complete visual understanding of the Barangay Reserve System architecture, data flow, and integration points for capstone presentation.
