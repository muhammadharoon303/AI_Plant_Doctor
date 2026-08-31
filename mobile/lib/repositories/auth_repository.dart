import '../core/network/api_client.dart';
import '../core/constants/app_constants.dart';
import '../models/user_model.dart';

class AuthRepository {
  final ApiClient _apiClient;

  AuthRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  Future<UserModel> register({
    required String email,
    required String password,
    String? fullName,
    String languagePreference = 'en',
  }) async {
    final response = await _apiClient.post(
      AppConstants.authRegisterEndpoint,
      body: {
        'email': email,
        'password': password,
        'full_name': fullName,
        'language_preference': languagePreference,
      },
    );
    return UserModel.fromJson(response);
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await _apiClient.post(
      AppConstants.authLoginEndpoint,
      body: {
        'email': email,
        'password': password,
      },
    );
    return {
      'token': response['access_token'],
      'user': UserModel.fromJson(response['user']),
    };
  }

  Future<String> forgotPassword(String email) async {
    final response = await _apiClient.post(
      '${AppConstants.apiBaseUrl}/auth/forgot-password',
      body: {'email': email},
    );
    return response['message'] ?? 'Password reset email sent.';
  }

  Future<UserModel> getMe(String token) async {
    final response = await _apiClient.get(
      AppConstants.authMeEndpoint,
      headers: {'Authorization': 'Bearer $token'},
    );
    return UserModel.fromJson(response);
  }
}
