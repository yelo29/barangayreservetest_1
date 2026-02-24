import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../services/api_service.dart';
import '../services/auth_api_service.dart';
import '../services/data_service.dart';
import '../dashboard/resident_dashboard.dart';
import '../screens/selection_screen.dart';

class ResidentLoginScreen extends StatefulWidget {
  const ResidentLoginScreen({super.key});

  @override
  State<ResidentLoginScreen> createState() => _ResidentLoginScreenState();
}

class _ResidentLoginScreenState extends State<ResidentLoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _contactController = TextEditingController();
  final TextEditingController _addressController = TextEditingController();

  bool _isLoading = false;
  bool _isSignUp = false;
  String? _errorMessage;
  Map<String, dynamic>? _currentUser;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _nameController.dispose();
    _contactController.dispose();
    _addressController.dispose();
    super.dispose();
  }

  Future<void> _signUp() async {
    if (_emailController.text.isEmpty || 
        _passwordController.text.isEmpty || 
        _nameController.text.isEmpty ||
        _contactController.text.isEmpty ||
        _addressController.text.isEmpty) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Please fill in all fields';
        });
      }
      return;
    }

    if (_passwordController.text.length < 6) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Password must be at least 6 characters';
        });
      }
      return;
    }

    if (mounted) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });
    }

    try {
      print('🔥 Starting server sign up process...');
      print('Email: ${_emailController.text.trim()}');
      print('Name: ${_nameController.text.trim()}');
      print('Contact: ${_contactController.text.trim()}');
      print('Address: ${_addressController.text.trim()}');
      
      final result = await ApiService.register(
        _nameController.text.trim(),
        _emailController.text.trim(),
        _passwordController.text.trim(),
        role: 'resident',
      );
      
      // Update profile with contact and address after successful registration
      if (result['success']) {
        try {
          final authApiService = AuthApiService.instance;
          await authApiService.signInWithEmailAndPassword(
            _emailController.text.trim(),
            _passwordController.text.trim(),
          );
          
          // Update profile with additional info
          await DataService.updateUserProfile({
            'contact_number': _contactController.text.trim(),
            'address': _addressController.text.trim(),
          });
        } catch (e) {
          print('❌ Error updating profile after registration: $e');
        }
      }
      
      if (result['success']) {
        print('✅ Server Registration successful!');
        
        // AUTO-LOGIN AFTER REGISTRATION
        print('🔥 Auto-logging in after registration...');
        final loginResult = await AuthApiService.instance.signInWithEmailAndPassword(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );
        
        if (loginResult['success'] && mounted) {
          print('✅ Auto-login successful!');
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => ResidentDashboard(onLogout: (context) async {
              print('🔥 Resident logout - clearing authentication data');
              
              // Clear authentication data
              await AuthApiService.instance.signOut();
              await ApiService.clearUserData();
              
              // Navigate back to selection screen
              if (context.mounted) {
                Navigator.pushReplacement(
                  context, 
                  MaterialPageRoute(builder: (_) => const SelectionScreen())
                );
              }
            })),
          );
        } else {
          print('❌ Auto-login failed: ${loginResult['message']}');
          if (mounted) {
            setState(() {
              _errorMessage = 'Registration successful but login failed. Please try logging in manually.';
            });
          }
        }
      } else {
        if (mounted) {
          setState(() {
            _errorMessage = result['message'] ?? 'Registration failed';
          });
        }
      }
    } catch (e) {
      print('❌ Server Registration error: $e');
      if (mounted) {
        setState(() {
          _errorMessage = 'Registration failed: ${e.toString()}';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _signIn() async {
    if (_emailController.text.isEmpty || _passwordController.text.isEmpty) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Please fill in all fields';
        });
      }
      return;
    }

    if (mounted) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });
    }

    try {
      print('🔥 Starting server sign in process...');
      print('Email: ${_emailController.text.trim()}');
      
      final result = await AuthApiService.instance.signInWithEmailAndPassword(
        _emailController.text.trim(),
        _passwordController.text.trim(),
      );
      
      if (result['success']) {
        print('✅ Server Login successful!');
        print('User role: ${result['user']['role']}');
        
        if (result['user']['role'] == 'resident') {
          if (mounted) {
            setState(() {
              _currentUser = result['user'];
            });
          }
          
          if (mounted) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (_) => ResidentDashboard(onLogout: (context) async {
                print('🔥 Resident logout - clearing authentication data');
                
                // Clear authentication data
                await AuthApiService.instance.signOut();
                await ApiService.clearUserData();
                
                // Navigate back to selection screen
                if (context.mounted) {
                  Navigator.pushReplacement(
                    context, 
                    MaterialPageRoute(builder: (_) => const SelectionScreen())
                  );
                }
              }, userData: result['user'])),
            );
          }
        } else {
          if (mounted) {
            setState(() {
              _errorMessage = 'This account is not a resident account';
            });
          }
        }
      } else {
        if (mounted) {
          setState(() {
            _errorMessage = result['message'] ?? 'Login failed';
          });
        }
      }
    } catch (e) {
      print('❌ Login error: $e');
      if (mounted) {
        setState(() {
          _errorMessage = 'An error occurred during login';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFFECACA), Color(0xFFDBEAFE)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          IconButton(
                            icon: const Icon(Icons.arrow_back),
                            onPressed: () => Navigator.pop(context),
                          ),
                          Text(_isSignUp ? "Resident Sign Up" : "Resident Login",
                              style: TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(18),
                          boxShadow: const [
                            BoxShadow(color: Colors.black12, blurRadius: 10)
                          ],
                        ),
                        child: Column(
                          children: [
                            if (_isSignUp) ...[
                              _buildTextField("Full Name", "Enter your full name", controller: _nameController, isName: true),
                              const SizedBox(height: 16),
                              _buildTextField("Contact Number", "Enter your contact number", controller: _contactController, isPhone: true),
                              const SizedBox(height: 16),
                              _buildTextField("Address", "Enter your address", controller: _addressController),
                              const SizedBox(height: 16),
                            ],
                            _buildTextField("Email Address", "Enter your email", controller: _emailController, isEmail: true),
                            const SizedBox(height: 16),
                            _buildTextField("Password", "Enter your password",
                                controller: _passwordController, obscure: true),
                            if (_errorMessage != null) ...[
                              const SizedBox(height: 12),
                              Container(
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: Colors.red[50],
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(_errorMessage!,
                                    style: TextStyle(color: Colors.red[700])),
                              ),
                            ],
                            const SizedBox(height: 24),
                            SizedBox(
                              width: double.infinity,
                              height: 50,
                              child: ElevatedButton(
                                onPressed: _isLoading ? null : (_isSignUp ? _signUp : _signIn),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.blue[600],
                                  foregroundColor: Colors.white,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                ),
                                child: _isLoading
                                    ? const CircularProgressIndicator(
                                        strokeWidth: 2,
                                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                      )
                                    : Text(_isSignUp ? "Sign Up" : "Sign In",
                                        style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w600,
                                            color: Colors.white)),
                              ),
                            ),
                            const SizedBox(height: 16),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(_isSignUp ? "Already have an account? " : "Don't have an account? ",
                                    style: TextStyle(color: Colors.grey[600])),
                                GestureDetector(
                                  onTap: () {
                                    if (mounted) {
                                      setState(() {
                                        _isSignUp = !_isSignUp;
                                        _errorMessage = null;
                                      });
                                    }
                                  },
                                  child: Text(_isSignUp ? "Sign In" : "Sign Up",
                                      style: TextStyle(
                                          color: Colors.blue,
                                          fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(String label, String hint, {bool obscure = false, TextEditingController? controller, bool isEmail = false, bool isName = false, bool isPhone = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
        const SizedBox(height: 6),
        TextField(
          controller: controller,
          obscureText: obscure,
          autofillHints: isEmail ? [AutofillHints.email] : 
                         isName ? [AutofillHints.name] :
                         isPhone ? [AutofillHints.telephoneNumber] :
                         obscure ? [AutofillHints.password] : null,
          keyboardType: isEmail ? TextInputType.emailAddress :
                      isPhone ? TextInputType.phone :
                      TextInputType.text,
          decoration: InputDecoration(
            hintText: hint,
            border:
                OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
          ),
        ),
      ],
    );
  }
}
