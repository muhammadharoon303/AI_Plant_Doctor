import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../repositories/auth_repository.dart';
import '../services/storage_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthRepository _repository;

  AuthProvider({AuthRepository? repository})
      : _repository = repository ?? AuthRepository();

  UserModel? _user;
  String? _token;
  bool _isLoading = false;
  bool _isInitialized = false;
  String? _errorMessage;

  UserModel? get user => _user;
  String? get token => _token;
  bool get isAuthenticated => _token != null && _user != null;
  bool get isLoading => _isLoading;
  bool get isInitialized => _isInitialized;
  String? get errorMessage => _errorMessage;

  Future<void> initSession() async {
    final storage = await StorageService.getInstance();
    _token = storage.userToken;
    _user = storage.userProfile;

    if (_token != null) {
      try {
        _user = await _repository.getMe(_token!);
        await storage.setUserProfile(_user!);
      } catch (_) {
        // Token expired or invalid, clear session
        await storage.clearAuthSession();
        _token = null;
        _user = null;
      }
    }

    _isInitialized = true;
    notifyListeners();
  }

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final data = await _repository.login(email: email, password: password);
      _token = data['token'];
      _user = data['user'];

      final storage = await StorageService.getInstance();
      await storage.setUserToken(_token!);
      await storage.setUserProfile(_user!);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = _cleanErrorMessage(e.toString());
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String password,
    String? fullName,
    String languagePreference = 'en',
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _repository.register(
        email: email,
        password: password,
        fullName: fullName,
        languagePreference: languagePreference,
      );
      // Auto-login after registration
      return await login(email, password);
    } catch (e) {
      _errorMessage = _cleanErrorMessage(e.toString());
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<String?> forgotPassword(String email) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final msg = await _repository.forgotPassword(email);
      _isLoading = false;
      notifyListeners();
      return msg;
    } catch (e) {
      _errorMessage = _cleanErrorMessage(e.toString());
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  Future<void> logout() async {
    final storage = await StorageService.getInstance();
    await storage.clearAuthSession();
    _token = null;
    _user = null;
    notifyListeners();
  }

  String _cleanErrorMessage(String err) {
    if (err.contains('Exception:')) {
      return err.replaceAll('Exception:', '').trim();
    }
    return err;
  }
}
