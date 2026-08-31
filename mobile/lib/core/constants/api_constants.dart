import 'package:shared_preferences/shared_preferences.dart';

class ApiConstants {
  static String _customUrl = '';

  static Future<void> loadCustomUrl() async {
    final prefs = await SharedPreferences.getInstance();
    _customUrl = prefs.getString('custom_server_url') ?? '';
  }

  static Future<void> setCustomServerUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('custom_server_url', url.trim());
    _customUrl = url.trim();
  }

  static String get baseUrl {
    if (_customUrl.isNotEmpty) {
      final clean = _customUrl.endsWith('/') ? _customUrl.substring(0, _customUrl.length - 1) : _customUrl;
      return clean.endsWith('/api/v1') ? clean : '$clean/api/v1';
    }
    return 'http://192.168.100.5:8000/api/v1';
  }

  static String get diagnoseEndpoint => '$baseUrl/diagnose';
  static String get diseasesEndpoint => '$baseUrl/diseases';
  static String get assistantEndpoint => '$baseUrl/assistant';
  static String get authEndpoint => '$baseUrl/auth';
  static String get plantsEndpoint => '$baseUrl/plants';
}
