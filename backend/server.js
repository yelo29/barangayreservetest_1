require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const admin = require('firebase-admin');

const FirebaseService = require('./firebase-service');

const app = express();
const PORT = process.env.PORT || 3000;
const firebaseService = new FirebaseService();

// Initialize Firebase Storage
const bucket = admin.storage().bucket();

// Middleware
app.use(cors({
  origin: [
    'http://localhost:3000',
    'http://192.168.100.4:3000',
    // Allow any origin for mobile testing
    /^http:\/\/192\.168\.\d+\.\d+(:\d+)?$/
  ],
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// File upload configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads/';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'), false);
    }
  }
});

// JWT Middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  console.log('🔍 Verifying token:', token.substring(0, 20) + '...');
  console.log('🔍 JWT_SECRET exists:', !!process.env.JWT_SECRET);
  console.log('🔍 JWT_SECRET length:', process.env.JWT_SECRET?.length);

  const jwtSecret = process.env.JWT_SECRET || 'barangay-reserve-super-secret-jwt-key-2024';
  console.log('🔍 Using JWT_SECRET:', jwtSecret.substring(0, 20) + '...');

  jwt.verify(token, jwtSecret, (err, user) => {
    if (err) {
      console.log('❌ Token verification error:', err.message);
      return res.status(403).json({ error: 'Invalid token' });
    }
    console.log('✅ Token verified successfully for user:', user);
    req.user = user;
    next();
  });
};

// Helper function to generate JWT
const generateToken = (user) => {
  const jwtSecret = process.env.JWT_SECRET || 'barangay-reserve-super-secret-jwt-key-2024';
  console.log('🔍 Using JWT_SECRET:', jwtSecret.substring(0, 20) + '...');
  
  try {
    const token = jwt.sign(
      { uid: user.uid, email: user.email, role: user.role },
      jwtSecret,
      { expiresIn: '24h' }
    );
    console.log('🔍 Token generated successfully');
    return token;
  } catch (error) {
    console.error('❌ Token generation error:', error);
    throw error;
  }
};

// Routes

// Health Check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Barangay Reserve API is running' });
});

// Authentication Routes
app.post('/api/auth/register', async (req, res) => {
  try {
    const { name, email, password, role = 'resident' } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ error: 'Name, email, and password are required' });
    }

    // Check if user already exists
    const existingUser = await firebaseService.getUserByEmail(email);
    if (existingUser.success) {
      return res.status(400).json({ error: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    const uid = uuidv4();

    // Create user
    const userData = {
      uid,
      name,
      email,
      password: hashedPassword,
      role,
      isAuthenticated: false,
      discount: 0.0,
      verificationType: 'unverified'
    };

    const result = await firebaseService.createUser(userData);
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    const token = generateToken(userData);
    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      token,
      user: { 
        uid, 
        name, 
        email, 
        role,
        isAuthenticated: false,
        discount: 0.0,
        verificationType: 'unverified'
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Get user from database
    const userResult = await firebaseService.getUserByEmail(email);
    if (!userResult.success) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const user = userResult.data;
    console.log('🔍 Found user:', { uid: user.uid, email: user.email, role: user.role });
    console.log('🔍 User has password field:', !!user.password);
    
    // Require password for all users - no auto-validation
    if (!user.password) {
      console.log('❌ User has no password field - rejecting login');
      return res.status(401).json({ error: 'Account not properly set up - please contact administrator' });
    }
    
    const isPasswordValid = await bcrypt.compare(password, user.password);
    console.log('🔍 Password valid:', isPasswordValid);

    if (!isPasswordValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    console.log('🔍 Generating token...');
    const token = generateToken(user);
    console.log('🔍 Token generated successfully');
    res.json({
      success: true,
      message: 'Login successful',
      token,
      user: { 
        uid: user.uid, 
        name: user.name, 
        email: user.email, 
        role: user.role,
        isAuthenticated: user.isAuthenticated || false,
        discount: user.discount || 0,
        verificationType: user.verificationType || 'unverified'
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Login failed' });
  }
});

// User Routes
app.get('/api/users/:uid', authenticateToken, async (req, res) => {
  try {
    const { uid } = req.params;
    const result = await firebaseService.getUser(uid);
    
    if (!result.success) {
      return res.status(404).json({ error: result.error });
    }

    // Remove password from response
    const { password, ...userWithoutPassword } = result.data;
    res.json({ success: true, user: userWithoutPassword });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Failed to get user' });
  }
});

// Facility Routes
app.get('/api/facilities', async (req, res) => {
  try {
    const result = await firebaseService.getAllFacilities();
    res.json(result);
  } catch (error) {
    console.error('Get facilities error:', error);
    res.status(500).json({ error: 'Failed to get facilities' });
  }
});

app.post('/api/facilities', authenticateToken, async (req, res) => {
  try {
    const facilityData = req.body;
    const result = await firebaseService.createFacility(facilityData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(201).json({
      message: 'Facility created successfully',
      facilityId: result.id
    });
  } catch (error) {
    console.error('Create facility error:', error);
    res.status(500).json({ error: 'Failed to create facility' });
  }
});

// Update user profile
app.put('/api/users/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const userData = req.body;
    
    // Users can only update their own profile
    if (req.user.uid !== id && req.user.id !== id) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.updateUserProfile(id, userData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(200).json({
      message: 'User profile updated successfully',
      user: result.user
    });
  } catch (error) {
    console.error('Update user profile error:', error);
    res.status(500).json({ error: 'Failed to update user profile' });
  }
});

app.put('/api/facilities/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const facilityData = req.body;
    const result = await firebaseService.updateFacility(id, facilityData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.json({ message: 'Facility updated successfully' });
  } catch (error) {
    console.error('Update facility error:', error);
    res.status(500).json({ error: 'Failed to update facility' });
  }
});

// Booking Routes
app.post('/api/bookings', authenticateToken, async (req, res) => {
  try {
    const bookingData = {
      ...req.body,
      userId: req.user.uid
    };
    
    const result = await firebaseService.createBooking(bookingData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(201).json({
      message: 'Booking created successfully',
      bookingId: result.id
    });
  } catch (error) {
    console.error('Create booking error:', error);
    res.status(500).json({ error: 'Failed to create booking' });
  }
});

// Get all bookings (with optional filtering)
app.get('/api/bookings', authenticateToken, async (req, res) => {
  try {
    const { user_email, user_role } = req.query;
    
    // If user_email is provided, get bookings for that user
    if (user_email) {
      // Users can only get their own bookings unless they're officials
      if (req.user.email !== user_email && req.user.role !== 'official') {
        return res.status(403).json({ error: 'Access denied' });
      }
      
      const result = await firebaseService.getUserBookingsByEmail(user_email);
      return res.json(result);
    }
    
    // If no user_email, officials can get all bookings, residents get empty
    if (req.user.role === 'official') {
      const snapshot = await firebaseService.db.collection('bookings').get();
      const bookings = [];
      snapshot.forEach(doc => {
        bookings.push({ id: doc.id, ...doc.data() });
      });
      return res.json(bookings);
    }
    
    // Residents get empty array if no user_email specified
    return res.json([]);
    
  } catch (error) {
    console.error('Get bookings error:', error);
    res.status(500).json({ error: 'Failed to get bookings' });
  }
});

// NEW: Get User Bookings by Email
app.get('/api/bookings/user/email/:email', authenticateToken, async (req, res) => {
  try {
    const { email } = req.params;
    
    // Users can only get their own bookings unless they're officials
    if (req.user.email !== email && req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.getUserBookingsByEmail(email);
    res.json(result);
  } catch (error) {
    console.error('Get user bookings by email error:', error);
    res.status(500).json({ error: 'Failed to get user bookings by email' });
  }
});

app.get('/api/bookings/user/:userId', authenticateToken, async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Users can only get their own bookings unless they're officials
    if (req.user.uid !== userId && req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.getUserBookings(userId);
    res.json(result);
  } catch (error) {
    console.error('Get user bookings error:', error);
    res.status(500).json({ error: 'Failed to get user bookings' });
  }
});

// Get all officials (for public access)
app.get('/api/officials', async (req, res) => {
  try {
    const snapshot = await firebaseService.db.collection('users')
      .where('role', '==', 'official')
      .get();
    
    const officials = [];
    snapshot.forEach(doc => {
      officials.push({
        id: doc.id,
        name: doc.data().name || 'Unknown',
        email: doc.data().email || '',
        role: doc.data().role || 'official'
      });
    });
    
    res.json(officials);
  } catch (error) {
    console.error('Get officials error:', error);
    res.status(500).json({ error: 'Failed to get officials' });
  }
});

// Get all booking requests (for officials)
app.get('/api/bookings/pending', authenticateToken, async (req, res) => {
  try {
    // Only officials can view all booking requests
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.getAllPendingBookings();
    res.json(result);
  } catch (error) {
    console.error('Get pending bookings error:', error);
    res.status(500).json({ error: 'Failed to get pending bookings' });
  }
});

app.get('/api/bookings/facility/:facilityId/:date', authenticateToken, async (req, res) => {
  try {
    const { facilityId, date } = req.params;
    const result = await firebaseService.getFacilityBookings(facilityId, date);
    res.json(result);
  } catch (error) {
    console.error('Get facility bookings error:', error);
    res.status(500).json({ error: 'Failed to get facility bookings' });
  }
});

// Debug endpoint to see all bookings
app.get('/api/debug/bookings', authenticateToken, async (req, res) => {
  try {
    const snapshot = await firebaseService.db.collection('bookings').get();
    const bookings = [];
    snapshot.forEach(doc => {
      bookings.push({ id: doc.id, ...doc.data() });
    });
    
    console.log(`🔍 DEBUG: All bookings in database (${bookings.length}):`);
    bookings.forEach(booking => {
      console.log(`   ${booking.email} - ${booking.facilityName} - ${booking.facilityId} - ${booking.bookingDate} - ${booking.status}`);
    });
    
    res.json({ success: true, bookings: bookings });
  } catch (error) {
    console.error('Debug bookings error:', error);
    res.status(500).json({ error: 'Failed to get debug bookings' });
  }
});

// Get all bookings for a facility in a date range (for calendar)
app.get('/api/bookings/facility/:facilityId/range/:startDate/:endDate', authenticateToken, async (req, res) => {
  try {
    const { facilityId, startDate, endDate } = req.params;
    const result = await firebaseService.getFacilityBookingsInRange(facilityId, startDate, endDate);
    res.json(result);
  } catch (error) {
    console.error('Get facility bookings in range error:', error);
    res.status(500).json({ error: 'Failed to get facility bookings in range' });
  }
});

// Get all pending authentication requests (for officials)
app.get('/api/authentication-requests/pending', authenticateToken, async (req, res) => {
  try {
    // Only officials can view all authentication requests
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.getPendingAuthenticationRequests();
    res.json(result);
  } catch (error) {
    console.error('Get pending authentication requests error:', error);
    res.status(500).json({ error: 'Failed to get pending authentication requests' });
  }
});

// Update authentication request status (for officials)
app.put('/api/authentication-requests/:id/status', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    // Only officials can update authentication request status
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.updateAuthenticationRequest(id, status, req.user.uid);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.json({ message: 'Authentication request updated successfully' });
  } catch (error) {
    console.error('Update authentication request error:', error);
    res.status(500).json({ error: 'Failed to update authentication request' });
  }
});

app.put('/api/bookings/:id/status', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    // Only officials can update booking status
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.updateBookingStatus(id, status, req.user.uid);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.json({ message: 'Booking status updated successfully' });
  } catch (error) {
    console.error('Update booking status error:', error);
    res.status(500).json({ error: 'Failed to update booking status' });
  }
});

// Receipt Upload Route
app.post('/api/upload/receipt', authenticateToken, upload.single('receipt'), async (req, res) => {
  try {
    console.log('🔍 Receipt upload request received');
    console.log('🔍 User:', req.user.email, 'Role:', req.user.role);
    console.log('🔍 File received:', req.file ? 'YES' : 'NO');
    
    if (!req.file) {
      console.log('❌ No receipt file uploaded');
      return res.status(400).json({ error: 'No receipt file uploaded' });
    }

    console.log('🔍 File details:', {
      originalname: req.file.originalname,
      mimetype: req.file.mimetype,
      size: req.file.size,
      buffer: req.file.buffer ? `${req.file.buffer.length} bytes` : 'NO BUFFER'
    });

    // Upload to Firebase Storage
    const fileName = `receipts/${req.user.uid}/${Date.now()}_${req.file.originalname}`;
    console.log('🔍 Uploading to Firebase Storage:', fileName);
    
    const fileUpload = bucket.file(fileName);

    await fileUpload.save(req.file.buffer, {
      metadata: {
        contentType: req.file.mimetype,
      },
    });

    // Get public URL
    const [url] = await fileUpload.getSignedUrl({
      action: 'read',
      expires: '03-01-2500', // Far future expiration
    });

    console.log('✅ Receipt uploaded successfully:', url);
    
    res.status(200).json({
      message: 'Receipt uploaded successfully',
      imageUrl: url,
    });
  } catch (error) {
    console.error('❌ Receipt upload error:', error);
    res.status(500).json({ error: 'Failed to upload receipt' });
  }
});

// Verification Image Upload Route
app.post('/api/upload/verification', authenticateToken, upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image file uploaded' });
    }

    const { type } = req.body; // 'profileImage' or 'idImage'

    // Upload to Firebase Storage
    const fileName = `verification/${req.user.uid}/${type}_${Date.now()}_${req.file.originalname}`;
    const fileUpload = bucket.file(fileName);

    await fileUpload.save(req.file.buffer, {
      metadata: {
        contentType: req.file.mimetype,
      },
    });

    // Get public URL
    const [url] = await fileUpload.getSignedUrl({
      action: 'read',
      expires: '03-01-2500', // Far future expiration
    });

    res.status(200).json({
      message: 'Verification image uploaded successfully',
      imageUrl: url,
    });
  } catch (error) {
    console.error('Verification image upload error:', error);
    res.status(500).json({ error: 'Failed to upload verification image' });
  }
});

// Authentication Request Routes
app.post('/api/authentication-requests', authenticateToken, upload.fields([
  { name: 'profileImage', maxCount: 1 },
  { name: 'idImage', maxCount: 1 }
]), async (req, res) => {
  try {
    const requestData = {
      ...req.body,
      userId: req.user.uid,
      profileImageUrl: req.files.profileImage ? `/uploads/${req.files.profileImage[0].filename}` : null,
      idImageUrl: req.files.idImage ? `/uploads/${req.files.idImage[0].filename}` : null,
      status: 'pending'
    };
    
    const result = await firebaseService.createAuthenticationRequest(requestData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(201).json({
      message: 'Authentication request submitted successfully',
      requestId: result.id
    });
  } catch (error) {
    console.error('Create authentication request error:', error);
    res.status(500).json({ error: 'Failed to submit authentication request' });
  }
});

app.get('/api/authentication-requests/pending', authenticateToken, async (req, res) => {
  try {
    // Only officials can view pending requests
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.getPendingAuthenticationRequests();
    res.json(result);
  } catch (error) {
    console.error('Get authentication requests error:', error);
    res.status(500).json({ error: 'Failed to get authentication requests' });
  }
});

app.put('/api/authentication-requests/:id/status', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    // Only officials can update request status
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const result = await firebaseService.updateAuthenticationRequest(id, status, req.user.uid);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.json({ message: 'Authentication request updated successfully' });
  } catch (error) {
    console.error('Update authentication request error:', error);
    res.status(500).json({ error: 'Failed to update authentication request' });
  }
});

// Barangay Events Routes
app.post('/api/barangay-events', authenticateToken, async (req, res) => {
  try {
    // Only officials can create events
    if (req.user.role !== 'official') {
      return res.status(403).json({ error: 'Access denied' });
    }

    const eventData = req.body;
    const result = await firebaseService.createBarangayEvent(eventData);
    
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(201).json({
      message: 'Barangay event created successfully',
      eventId: result.id
    });
  } catch (error) {
    console.error('Create barangay event error:', error);
    res.status(500).json({ error: 'Failed to create barangay event' });
  }
});

app.get('/api/barangay-events', async (req, res) => {
  try {
    const result = await firebaseService.getBarangayEvents();
    res.json(result);
  } catch (error) {
    console.error('Get barangay events error:', error);
    res.status(500).json({ error: 'Failed to get barangay events' });
  }
});

// Serve uploaded files
app.use('/uploads', express.static('uploads'));

// Error handling middleware
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File size too large. Maximum size is 5MB.' });
    }
  }
  if (error.message === 'Only image files are allowed') {
    return res.status(400).json({ error: error.message });
  }
  console.error('Unhandled error:', error);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Barangay Reserve API server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 Local API URL: http://localhost:${PORT}/api`);
  console.log(`🌐 Network API URL: http://192.168.100.4:${PORT}/api`);
});

module.exports = app;
