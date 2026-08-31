class AppConstants {
  static const String appName = 'AI Plant Doctor';
  static const String appVersion = '1.0.0';

  // API Base URL (Configurable per environment)
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1',
  );

  // Endpoints
  static const String authRegisterEndpoint = '$apiBaseUrl/auth/register';
  static const String authLoginEndpoint = '$apiBaseUrl/auth/token';
  static const String authMeEndpoint = '$apiBaseUrl/auth/me';
  static const String diagnoseEndpoint = '$apiBaseUrl/diagnose';
  static const String diseasesEndpoint = '$apiBaseUrl/diseases';
  static const String plantsEndpoint = '$apiBaseUrl/plants';
  static const String assistantEndpoint = '$apiBaseUrl/assistant';
  static const String adminEndpoint = '$apiBaseUrl/admin';

  // Timeouts & Durations
  static const int connectTimeoutSeconds = 15;
  static const int receiveTimeoutSeconds = 30;

  // Supported Languages
  static const String langEnglish = 'en';
  static const String langUrdu = 'ur';
  static const String langPashto = 'ps';
}
