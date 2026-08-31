import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';

class StorageService {
  static const String _keyOnboardingCompleted = 'is_onboarding_completed';
  static const String _keyLanguageCode = 'language_code';
  static const String _keyThemeMode = 'theme_mode';
  static const String _keyUserToken = 'user_token';
  static const String _keyUserProfile = 'user_profile';

  static StorageService? _instance;
  static SharedPreferences? _prefs;

  StorageService._();

  static Future<StorageService> getInstance() async {
    _instance ??= StorageService._();
    _prefs ??= await SharedPreferences.getInstance();
    return _instance!;
  }

  // Onboarding status
  bool get isOnboardingCompleted => _prefs?.getBool(_keyOnboardingCompleted) ?? false;

  Future<bool> setOnboardingCompleted(bool value) async {
    return await _prefs?.setBool(_keyOnboardingCompleted, value) ?? false;
  }

  // Language preference
  String? get languageCode => _prefs?.getString(_keyLanguageCode);

  Future<bool> setLanguageCode(String code) async {
    return await _prefs?.setString(_keyLanguageCode, code) ?? false;
  }

  // Theme preference
  String? get themeMode => _prefs?.getString(_keyThemeMode);

  Future<bool> setThemeMode(String mode) async {
    return await _prefs?.setString(_keyThemeMode, mode) ?? false;
  }

  // Auth Token
  String? get userToken => _prefs?.getString(_keyUserToken);

  Future<bool> setUserToken(String token) async {
    return await _prefs?.setString(_keyUserToken, token) ?? false;
  }

  // User Profile
  UserModel? get userProfile {
    final rawJson = _prefs?.getString(_keyUserProfile);
    if (rawJson != null && rawJson.isNotEmpty) {
      try {
        return UserModel.fromJson(jsonDecode(rawJson));
      } catch (_) {
        return null;
      }
    }
    return null;
  }

  Future<bool> setUserProfile(UserModel user) async {
    return await _prefs?.setString(_keyUserProfile, jsonEncode(user.toJson())) ?? false;
  }

  // Clear Session
  Future<void> clearAuthSession() async {
    await _prefs?.remove(_keyUserToken);
    await _prefs?.remove(_keyUserProfile);
  }
}
