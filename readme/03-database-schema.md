# Database Schema Documentation

## 🗄️ SQLite Database Structure

### **Database File**: `barangay.db`

---

## 📋 USERS TABLE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('resident', 'official')),
    verified INTEGER DEFAULT 0 CHECK (verified IN (0, 1)),
    discount_rate REAL DEFAULT 0.0 CHECK (discount_rate >= 0.0 AND discount_rate <= 1.0),
    contact_number TEXT DEFAULT '',
    address TEXT DEFAULT '',
    profile_photo_url TEXT,
    is_banned INTEGER DEFAULT 0 CHECK (is_banned IN (0, 1)),
    ban_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### **User Table Fields**:
- **id**: Unique user identifier
- **email**: User email (unique login identifier)
- **full_name**: User's complete name
- **password**: Hashed password for authentication
- **role**: User role ('resident' or 'official')
- **verified**: Verification status (0=unverified, 1=verified)
- **discount_rate**: Discount percentage (0.0 to 1.0)
- **contact_number**: Phone number for contact
- **address**: Residential address
- **profile_photo_url**: Profile image URL
- **is_banned**: Ban status (0=active, 1=banned)
- **ban_reason**: Reason for user ban
- **created_at**: Account creation timestamp
- **updated_at**: Last update timestamp

---

## 🏛️ FACILITIES TABLE

```sql
CREATE TABLE facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    capacity INTEGER DEFAULT 1,
    hourly_rate REAL NOT NULL DEFAULT 0.0,
    downpayment_rate REAL DEFAULT 0.5,
    image_url TEXT,
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### **Facility Table Fields**:
- **id**: Unique facility identifier
- **name**: Facility name (e.g., "Basketball Court", "Multi-Purpose Hall")
- **description**: Detailed facility description
- **capacity**: Maximum simultaneous users
- **hourly_rate**: Cost per hour
- **downpayment_rate**: Required downpayment percentage
- **image_url**: Facility photo URL
- **is_active**: Availability status (0=inactive, 1=active)
- **created_at**: Facility creation timestamp
- **updated_at**: Last modification timestamp

---

## 📅 BOOKINGS TABLE

```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    user_email TEXT NOT NULL,
    date TEXT NOT NULL,
    timeslot TEXT NOT NULL,
    purpose TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    payment_details TEXT,
    receipt_base64 TEXT,
    contact_number TEXT DEFAULT '',
    address TEXT DEFAULT '',
    total_amount REAL,
    downpayment REAL,
    rejection_reason TEXT,
    rejection_type TEXT,
    violation_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    FOREIGN KEY (user_email) REFERENCES users(email)
);
```

### **Booking Table Fields**:
- **id**: Unique booking identifier
- **facility_id**: Reference to booked facility
- **user_email**: Reference to user who made booking
- **date**: Booking date (YYYY-MM-DD format)
- **timeslot**: Time slot (e.g., "09:00-10:00")
- **purpose**: Booking purpose description
- **status**: Booking status ('pending', 'approved', 'rejected', 'cancelled')
- **payment_details**: Payment information
- **receipt_base64**: Base64 encoded receipt image
- **contact_number**: Contact number for booking
- **address**: Address for booking
- **total_amount**: Total booking cost
- **downpayment**: Downpayment amount
- **rejection_reason**: Reason for rejection
- **rejection_type**: Type of rejection
- **violation_count**: Number of violations
- **created_at**: Booking creation timestamp
- **updated_at**: Last status update timestamp

---

## 📋 VERIFICATION_REQUESTS TABLE

```sql
CREATE TABLE verification_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    id_type TEXT NOT NULL,
    id_number TEXT NOT NULL,
    id_image_base64 TEXT,
    profile_photo_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    notes TEXT,
    rejection_reason TEXT,
    discount_rate REAL DEFAULT 0.0,
    reviewed_by TEXT,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_email) REFERENCES users(email)
);
```

### **Verification Request Table Fields**:
- **id**: Unique verification request identifier
- **user_email**: Reference to user requesting verification
- **full_name**: Full legal name
- **address**: Residential address
- **contact_number**: Contact phone number
- **id_type**: ID type (e.g., "Driver's License", "Passport")
- **id_number**: ID document number
- **id_image_base64**: Base64 encoded ID image
- **profile_photo_url**: Profile photograph URL
- **status**: Verification status ('pending', 'approved', 'rejected')
- **notes**: Additional verification notes
- **rejection_reason**: Reason for rejection
- **discount_rate**: Approved discount rate
- **reviewed_by**: Official who reviewed request
- **reviewed_at**: Verification completion timestamp
- **created_at**: Request submission timestamp
- **updated_at**: Last modification timestamp

---

## 🏛️ AVAILABLE_TIMESLOTS TABLE

```sql
CREATE TABLE available_timeslots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    timeslot TEXT NOT NULL,
    is_available INTEGER DEFAULT 1 CHECK (is_available IN (0, 1)),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    UNIQUE(facility_id, date, timeslot)
);
```

### **Available Timeslots Table Fields**:
- **id**: Unique timeslot identifier
- **facility_id**: Reference to facility
- **date**: Date for timeslot (YYYY-MM-DD)
- **timeslot**: Time range (e.g., "09:00-10:00")
- **is_available**: Availability status (0=booked, 1=available)
- **created_at**: Timeslot creation timestamp
- **updated_at**: Last update timestamp

---

## 🔗 DATABASE RELATIONSHIPS

### **Primary Relationships**:
1. **Users → Bookings**: One-to-many (user can have many bookings)
2. **Facilities → Bookings**: One-to-many (facility can have many bookings)
3. **Users → Verification Requests**: One-to-many (user can have one verification)
4. **Facilities → Available Timeslots**: One-to-many (facility has many timeslots)

### **Foreign Key Constraints**:
- **bookings.facility_id** → **facilities.id**
- **bookings.user_email** → **users.email**
- **verification_requests.user_email** → **users.email**
- **available_timeslots.facility_id** → **facilities.id**

---

## 📊 INDEXES FOR PERFORMANCE

```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_banned ON users(is_banned);

-- Booking queries
CREATE INDEX idx_bookings_user ON bookings(user_email);
CREATE INDEX idx_bookings_facility ON bookings(facility_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_date ON bookings(date);

-- Verification queries
CREATE INDEX idx_verification_user ON verification_requests(user_email);
CREATE INDEX idx_verification_status ON verification_requests(status);

-- Facility queries
CREATE INDEX idx_facilities_active ON facilities(is_active);

-- Timeslot queries
CREATE INDEX idx_timeslots_facility ON available_timeslots(facility_id);
CREATE INDEX idx_timeslots_date ON available_timeslots(date);
CREATE INDEX idx_timeslots_available ON available_timeslots(is_available);
```

---

## 🛡️ DATA INTEGRITY

### **Constraints**:
- **UNIQUE**: User emails must be unique
- **CHECK**: Role must be 'resident' or 'official'
- **CHECK**: Status values limited to predefined options
- **CHECK**: Boolean fields use 0/1 values
- **CHECK**: Discount rates between 0.0 and 1.0
- **FOREIGN KEY**: Referential integrity maintained

### **Business Rules**:
1. **Ban System**: Banned users cannot create bookings
2. **Verification**: Only verified users get discounts
3. **Booking Limits**: One booking per timeslot per facility
4. **Time Slot Management**: Automatic availability updates
5. **Audit Trail**: All changes timestamped

---

## 🔄 DATABASE MIGRATION

### **Current Version**: v2.0
### **Previous Versions**:
- **v1.0**: Basic user and booking tables
- **v1.5**: Added verification system
- **v2.0**: Added ban system and enhanced constraints

### **Migration Scripts**:
- **v1_to_v2.sql**: Add ban fields and constraints
- **v2_to_future.sql**: Prepared for future enhancements

---

## 📈 USAGE STATISTICS

### **Common Queries**:
1. **User Bookings**: `SELECT * FROM bookings WHERE user_email = ?`
2. **Facility Availability**: `SELECT * FROM available_timeslots WHERE facility_id = ? AND date = ?`
3. **Pending Verifications**: `SELECT * FROM verification_requests WHERE status = 'pending'`
4. **User Status**: `SELECT * FROM users WHERE email = ? AND is_banned = 0`

### **Performance Optimizations**:
- **Indexes**: All frequently queried columns indexed
- **Constraints**: Database-level validation
- **Foreign Keys**: Referential integrity
- **Timestamps**: Audit trail capability
