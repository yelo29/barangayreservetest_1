# Barangay Reserve Backend API

A Node.js Express API for the Barangay Reserve application that provides secure backend services for user management, facility booking, and authentication requests.

## 🚀 Features

- **User Authentication**: Registration, login with JWT tokens
- **Role-based Access Control**: Residents and Officials with different permissions
- **Facility Management**: CRUD operations for facilities
- **Booking System**: Create, view, and manage bookings
- **Authentication Requests**: ID verification with image uploads
- **Barangay Events**: Community event management
- **File Uploads**: Image upload for authentication and facilities
- **Firebase Integration**: Secure database operations

## 📋 Prerequisites

- Node.js 16+ installed
- Firebase project set up with Firestore
- Firebase service account key

## 🛠️ Installation

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Firebase credentials:
   ```env
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n"
   FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxx@your-project-id.iam.gserviceaccount.com
   JWT_SECRET=your-super-secret-jwt-key
   PORT=3000
   ```

4. **Add Firebase service account key**
   - Download service account key from Firebase Console
   - Save as `firebase-service-account.json` in backend directory

5. **Start the server**
   ```bash
   # Development
   npm run dev
   
   # Production
   npm start
   ```

## 📊 Database Setup

The API will automatically create the following collections in Firestore:

### Collections Structure

#### `users`
```javascript
{
  uid: "string",
  name: "string",
  email: "string",
  password: "hashed_string",
  role: "resident|official",
  isAuthenticated: boolean,
  discount: number,
  verificationType: "unverified|resident|non-resident",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

#### `facilities`
```javascript
{
  id: "string",
  name: "string",
  description: "string",
  capacity: "string",
  rate: "string",
  downpayment: "string",
  amenities: "string",
  icon: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

#### `bookings`
```javascript
{
  id: "string",
  userId: "string",
  facilityId: "string",
  facilityName: "string",
  bookingDate: "string",
  timeslot: "string",
  fullName: "string",
  contactNumber: "string",
  address: "string",
  receiptImageURL: "string",
  status: "pending|approved|rejected|completed",
  submittedDate: timestamp,
  approvedDate: timestamp,
  approvedBy: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

#### `authenticationRequests`
```javascript
{
  id: "string",
  userId: "string",
  fullName: "string",
  address: "string",
  profileImageUrl: "string",
  idImageUrl: "string",
  verificationType: "resident|non-resident",
  status: "pending|approved|rejected",
  requestDate: timestamp,
  approvedDate: timestamp,
  approvedBy: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

#### `barangayEvents`
```javascript
{
  id: "string",
  title: "string",
  description: "string",
  eventDate: "string",
  eventTime: "string",
  location: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Users
- `GET /api/users/:uid` - Get user profile

### Facilities
- `GET /api/facilities` - Get all facilities
- `POST /api/facilities` - Create facility (official only)
- `PUT /api/facilities/:id` - Update facility (official only)

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/user/:userId` - Get user bookings
- `GET /api/bookings/facility/:facilityId/:date` - Get facility bookings for date
- `PUT /api/bookings/:id/status` - Update booking status (official only)

### Authentication Requests
- `POST /api/authentication-requests` - Submit authentication request
- `GET /api/authentication-requests/pending` - Get pending requests (official only)
- `PUT /api/authentication-requests/:id/status` - Update request status (official only)

### Barangay Events
- `POST /api/barangay-events` - Create event (official only)
- `GET /api/barangay-events` - Get all events

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Role-based Access**: Different permissions for residents vs officials
- **File Upload Security**: Image validation and size limits
- **CORS Protection**: Configurable CORS settings

## 📝 Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "resident"
  }'
```

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Create a booking (with token)
```bash
curl -X POST http://localhost:3000/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "facilityId": "facility123",
    "facilityName": "Basketball Court",
    "bookingDate": "2024-01-30",
    "timeslot": "9:00 AM - 10:00 AM",
    "fullName": "John Doe",
    "contactNumber": "1234567890",
    "address": "123 Main St",
    "receiptImageURL": "http://example.com/receipt.jpg"
  }'
```

## 🚀 Deployment

### Production Setup
1. Set `NODE_ENV=production` in `.env`
2. Use a process manager like PM2:
   ```bash
   npm install -g pm2
   pm2 start server.js --name "barangay-api"
   ```

### Environment Variables
- `NODE_ENV` - Development or production
- `PORT` - Server port (default: 3000)
- `JWT_SECRET` - Secret for JWT signing
- `FRONTEND_URL` - Frontend URL for CORS

## 🐛 Troubleshooting

### Common Issues
1. **Firebase Connection Error**: Check service account key and project ID
2. **JWT Token Error**: Verify JWT_SECRET is set
3. **File Upload Error**: Check upload directory permissions
4. **CORS Error**: Verify FRONTEND_URL matches your Flutter app URL

### Logs
```bash
# View logs
pm2 logs barangay-api

# Monitor
pm2 monit
```

## 📞 Support

For issues with:
- **Firebase Setup**: Check Firebase Console configuration
- **API Issues**: Check server logs and environment variables
- **Database Issues**: Verify Firestore rules and indexes

## 🔄 Next Steps

1. Set up Firebase project and service account
2. Configure environment variables
3. Start the backend server
4. Update Flutter app to use API endpoints
5. Test all functionality

The backend provides a secure, scalable foundation for your Barangay Reserve application!
