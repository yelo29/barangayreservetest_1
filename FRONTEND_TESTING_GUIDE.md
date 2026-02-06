# Frontend Testing Guide - Color-Coded Calendar & Time Slots

## 🎯 **TEST DATA OVERVIEW**

The database is now populated with **comprehensive test data** covering all frontend features and color scenarios.

---

## 📊 **CURRENT DATABASE STATUS**

### **Users (8 accounts)**
```
👤 Officials:
  - captain@barangay.gov / tatalaPunongBarangayadmin (Punong Barangay, verified, 0% discount)
  - secretary@barangay.gov / tatalaSecretaryadmin (Barangay Secretary, verified, 0% discount)
  - administrator@barangay.gov / tatalaAdministratoradmin (Barangay Administrator, verified, 0% discount)
  - kagawad1@barangay.gov / tatalaKagawad1admin (Councilor - Bookings, verified, 0% discount)
  - planning@barangay.gov / tatalaPlanningOfficeradmin (Planning Officer, verified, 0% discount)
  - utility@barangay.gov / tatalaUtilityadmin (Utility Worker, verified, 0% discount)

👥 Residents:
  - leo052904@gmail.com / zepol052904 (verified, 10% discount)
  - saloestillopez@gmail.com / salo3029 (verified, 5% discount)
  - resident@barangay.com / password123 (unverified, 0% discount)
```

### **Facilities (5 available)**
- Covered Court (₱75/hour)
- Meeting Room (₱30/hour)
- Multi-Purpose Hall (₱100/hour)
- Community Garden (₱25/hour)
- Basketball Court (₱50/hour)

### **Bookings (19 total)**
- **Approved**: 9 bookings
- **Pending**: 10 bookings
- **Date Range**: Jan 29 - Feb 17, 2026

---

## 🎨 **CALENDAR COLOR TESTING SCENARIOS**

### **🔘 GRAY Days (Past Dates - Disabled)**
```
📅 January 29, 2026
├── Covered Court 09:00 - approved (leo052904@gmail.com)
└── Meeting Room 14:00 - approved (saloestillopez@gmail.com)

✅ FRONTEND BEHAVIOR:
- Day appears GRAY in calendar
- Cannot tap/select the date
- Shows "Past date" or disabled state
- No time slot selection available
```

### **🔘 WHITE Days (Available - Enabled)**
```
📅 February 9, 2026 (and other available dates)
├── No bookings scheduled
└── All time slots available

✅ FRONTEND BEHAVIOR:
- Day appears WHITE in calendar
- Can tap/select the date
- Shows available time slots
- All time slots appear WHITE (available)
```

### **🔘 YELLOW Days (Pending Bookings - Enabled)**
```
📅 February 3, 2026 (Today)
├── Multi-Purpose Hall 08:00 - approved (captain@barangay.gov) → GREEN
├── Covered Court 10:00 - pending (leo052904@gmail.com) → YELLOW
└── Covered Court 10:00 - pending (saloestillopez@gmail.com) → YELLOW

📅 February 5, 2026
├── Meeting Room 09:00 - pending (leo052904@gmail.com) → YELLOW
├── Meeting Room 09:00 - pending (saloestillopez@gmail.com) → YELLOW
└── Meeting Room 09:00 - pending (resident@barangay.com) → YELLOW

✅ FRONTEND BEHAVIOR:
- Day appears YELLOW in calendar
- Can tap/select the date
- Shows mixed time slot colors
- Pending bookings visible but still selectable
```

### **🔘 GREEN Days (Approved/Official - Disabled)**
```
📅 February 6, 2026
├── Multi-Purpose Hall 13:00 - approved (captain@barangay.gov)
└── Covered Court 15:00 - approved (secretary@barangay.gov)

✅ FRONTEND BEHAVIOR:
- Day appears GREEN in calendar
- Cannot tap/select the date
- Shows "Booked" or "Official event"
- Time slots disabled for that date
```

---

## ⏰ **TIME SLOT COLOR TESTING SCENARIOS**

### **For leo052904@gmail.com (Verified Resident - 10% discount)**

#### **🔘 WHITE Time Slots (Available)**
```
📅 February 9, 2026 - Covered Court
├── 06:00-07:00 - WHITE (available)
├── 07:00-08:00 - WHITE (available)
├── 08:00-09:00 - WHITE (available)
└── All other slots - WHITE (available)

✅ FRONTEND BEHAVIOR:
- Time slot appears WHITE
- Can select and book
- Shows "Available" status
- Normal selection flow
```

#### **🔘 YELLOW Time Slots (User's Pending)**
```
📅 February 3, 2026 - Covered Court
└── 10:00-11:00 - YELLOW (user's pending booking)

📅 February 4, 2026 - Community Garden
└── 08:00-09:00 - YELLOW (user's pending booking)

✅ FRONTEND BEHAVIOR:
- Time slot appears YELLOW
- Can still select (modify/cancel option)
- Shows "Your pending booking" status
- Displays pending icon
```

#### **🔘 GREEN Time Slots (User's Approved)**
```
📅 February 7, 2026 - Covered Court
└── 14:00-15:00 - GREEN (user's approved booking)

✅ FRONTEND BEHAVIOR:
- Time slot appears GREEN
- Cannot select (disabled)
- Shows "Your approved booking" status
- Displays approved checkmark
```

#### **🏆 Competitive Time Slots**
```
📅 February 5, 2026 - Meeting Room
└── 09:00-10:00 - WHITE with competitive indicator
   ├── leo052904@gmail.com - pending
   ├── saloestillopez@gmail.com - pending
   └── resident@barangay.com - pending

✅ FRONTEND BEHAVIOR:
- Time slot appears WHITE (available)
- Shows competitive indicator (people icon)
- Can select to compete
- Shows "3 users competing" status
```

---

## 👥 **USER ROLE TESTING SCENARIOS**

### **👤 Official Users (captain@barangay.gov)**

#### **Calendar View**
```
✅ Can see ALL bookings regardless of user
✅ Days show combined status (highest priority)
✅ Can tap any date (including past for reference)
✅ See booking details in calendar tooltips
```

#### **Booking Management**
```
✅ See all pending bookings (10 total)
✅ Can approve/reject any booking
✅ Competitive booking resolution:
   - Approve one → Auto-reject others
   - Real-time status updates
✅ Full booking details visible
```

#### **Time Slot View**
```
✅ See all user bookings for each slot
✅ Can see competitive scenarios
✅ Full booking history visible
✅ Management controls available
```

### **👥 Resident Users (leo052904@gmail.com)**

#### **Calendar View**
```
✅ See only color-coded availability
✅ Cannot see other users' booking details
✅ Privacy protection maintained
✅ Can only book available slots
```

#### **Booking Management**
```
✅ See only own bookings (3 total)
✅ Can cancel own pending bookings
✅ Cannot modify approved bookings
✅ Personal booking history only
```

#### **Time Slot View**
```
✅ See personal booking status only
✅ Competitive indicators (but no details)
✅ Can book available slots
✅ Proper color coding for own bookings
```

---

## 💰 **DISCOUNT SYSTEM TESTING**

### **Pricing Calculations**
```
📊 Covered Court (₱75/hour) - 1 hour booking:

👤 resident@barangay.com (unverified):
  Base: ₱75.00
  Discount: 0%
  Total: ₱75.00
  Downpayment: ₱37.50

👥 saloestillopez@gmail.com (verified non-resident):
  Base: ₱75.00
  Discount: 5% (₱3.75)
  Total: ₱71.25
  Downpayment: ₱35.63

👥 leo052904@gmail.com (verified resident):
  Base: ₱75.00
  Discount: 10% (₱7.50)
  Total: ₱67.50
  Downpayment: ₱33.75
```

### **Frontend Display**
```
✅ Discount applied automatically
✅ Shows original vs. discounted price
✅ Displays discount percentage
✅ Calculates downpayment correctly
✅ Shows savings amount
```

---

## 🏆 **COMPETITIVE BOOKING TESTING**

### **Scenario 1: Meeting Room - Feb 5, 09:00**
```
📋 Current Status:
├── leo052904@gmail.com - pending
├── saloestillopez@gmail.com - pending
└── resident@barangay.com - pending

🎯 Official Action:
1. Login as captain@barangay.gov
2. Navigate to Feb 5, 2026
3. View Meeting Room 09:00 slot
4. See 3 competing bookings
5. Approve leo052904@gmail.com
6. Auto-reject others

✅ Frontend Updates:
- Leo sees: YELLOW → GREEN (approved)
- Salo sees: YELLOW → WHITE (available again)
- Resident sees: YELLOW → WHITE (available again)
- Calendar: YELLOW → GREEN (official approved)
```

### **Scenario 2: Covered Court - Feb 3, 10:00**
```
📋 Current Status:
├── leo052904@gmail.com - pending
└── saloestillopez@gmail.com - pending

🎯 Testing Flow:
1. Login as leo052904@gmail.com
2. See YELLOW time slot (own pending)
3. Can cancel or wait for approval
4. Login as saloestillopez@gmail.com
5. See YELLOW time slot (own pending)
6. Same competitive scenario

✅ Frontend Behavior:
- Both users see YELLOW (their pending)
- Both can cancel their bookings
- Official sees both pending bookings
- First approval wins the slot
```

---

## 📱 **FRONTEND FEATURE TESTING CHECKLIST**

### **🗓️ Calendar Features**
```
✅ Past dates appear GRAY and disabled
✅ Available dates appear WHITE and enabled
✅ Pending dates appear YELLOW and enabled
✅ Approved dates appear GREEN and disabled
✅ Month navigation works correctly
✅ Today button functions properly
✅ Date selection feedback works
✅ Color legend displays correctly
```

### **⏰ Time Slot Features**
```
✅ Available slots appear WHITE
✅ User's pending slots appear YELLOW
✅ User's approved slots appear GREEN (disabled)
✅ Competitive slots show indicators
✅ Slot selection works properly
✅ Status descriptions display
✅ Disabled slots cannot be selected
✅ Visual feedback for all states
```

### **👤 User Features**
```
✅ Login works for all 5 accounts
✅ Role-based access control
✅ Privacy protection for residents
✅ Full visibility for officials
✅ Personal booking management
✅ Discount system works correctly
✅ Verification request system
✅ Profile management
```

### **🏆 Competitive Booking**
```
✅ Multiple users can book same slot
✅ First-approved-wins logic
✅ Auto-rejection of competitors
✅ Real-time status updates
✅ Competitive indicators
✅ Official approval workflow
✅ Audit trail logging
✅ Fair competition system
```

---

## 🚀 **TESTING INSTRUCTIONS**

### **1. Start Backend Server**
```bash
cd server
python run_server.py
```

### **2. Run Flutter App**
```bash
flutter run
```

### **3. Test Scenarios**
```
📱 Test as Resident (leo052904@gmail.com):
  - Login and view calendar
  - Check color-coded dates
  - Try booking available slots
  - View own pending/approved bookings
  - Test discount calculations

📱 Test as Official (captain@barangay.gov):
  - Login and view all bookings
  - Approve/reject pending bookings
  - Test competitive booking resolution
  - Manage verification requests
  - Check system analytics
```

### **4. Validate Colors**
```
🎨 Calendar Colors:
  - GRAY: Past dates (Jan 29)
  - WHITE: Available dates (Feb 9)
  - YELLOW: Pending dates (Feb 3, 4, 5, 7, 8, 10)
  - GREEN: Approved dates (Feb 6)

⏰ Time Slot Colors:
  - WHITE: Available slots
  - YELLOW: User's pending bookings
  - GREEN: User's approved bookings
  - Competitive indicators for multiple bookings
```

---

## ✅ **TESTING VALIDATION**

The database is **fully populated** with comprehensive test data that covers:

1. **✅ All Calendar Color Scenarios**: GRAY, WHITE, YELLOW, GREEN
2. **✅ All Time Slot Color Scenarios**: WHITE, YELLOW, GREEN
3. **✅ Competitive Booking**: Multiple users same slot
4. **✅ User Role Testing**: Officials vs Residents
5. **✅ Discount System**: 0%, 5%, 10% scenarios
6. **✅ Verification Workflow**: Pending and approved requests
7. **✅ Privacy Protection**: Role-based data visibility
8. **✅ Real-time Updates**: Status change propagation

**The frontend is now ready for comprehensive testing with realistic data that will validate all color-coded calendar and time slot features!** 🎯✨
