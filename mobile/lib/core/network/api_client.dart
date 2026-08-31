import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../errors/app_exception.dart';
import '../constants/app_constants.dart';

class ApiClient {
  final http.Client _client;

  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  Future<Map<String, dynamic>> get(String url, {Map<String, String>? headers}) async {
    try {
      final response = await _client
          .get(Uri.parse(url), headers: _buildHeaders(headers))
          .timeout(const Duration(seconds: AppConstants.connectTimeoutSeconds));
      return _processResponse(response);
    } on SocketException {
      throw NetworkException();
    } on http.ClientException {
      throw NetworkException('Connection failed');
    }
  }

  Future<Map<String, dynamic>> post(
    String url, {
    Map<String, String>? headers,
    Object? body,
  }) async {
    try {
      final response = await _client
          .post(
            Uri.parse(url),
            headers: _buildHeaders(headers),
            body: body is String ? body : jsonEncode(body),
          )
          .timeout(const Duration(seconds: AppConstants.connectTimeoutSeconds));
      return _processResponse(response);
    } on SocketException {
      throw NetworkException();
    } on http.ClientException {
      throw NetworkException('Connection failed');
    }
  }

  Future<Map<String, dynamic>> put(
    String url, {
    Map<String, String>? headers,
    Object? body,
  }) async {
    try {
      final response = await _client
          .put(
            Uri.parse(url),
            headers: _buildHeaders(headers),
            body: body is String ? body : jsonEncode(body),
          )
          .timeout(const Duration(seconds: AppConstants.connectTimeoutSeconds));
      return _processResponse(response);
    } on SocketException {
      throw NetworkException();
    } on http.ClientException {
      throw NetworkException('Connection failed');
    }
  }

  Future<Map<String, dynamic>> delete(
    String url, {
    Map<String, String>? headers,
  }) async {
    try {
      final response = await _client
          .delete(Uri.parse(url), headers: _buildHeaders(headers))
          .timeout(const Duration(seconds: AppConstants.connectTimeoutSeconds));
      return _processResponse(response);
    } on SocketException {
      throw NetworkException();
    } on http.ClientException {
      throw NetworkException('Connection failed');
    }
  }

  Map<String, String> _buildHeaders(Map<String, String>? customHeaders) {
    final headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};
    if (customHeaders != null) {
      headers.addAll(customHeaders);
    }
    return headers;
  }

  Map<String, dynamic> _processResponse(http.Response response) {
    final body = response.body.isNotEmpty ? jsonDecode(utf8.decode(response.bodyBytes)) : {};
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (body is Map<String, dynamic>) {
        return body;
      }
      return {'data': body};
    } else if (response.statusCode == 401) {
      throw AuthException(body['detail'] ?? 'Unauthorized');
    } else if (response.statusCode >= 500) {
      throw ServerException(body['detail'] ?? 'Server Error');
    } else {
      throw ApiException(body['detail'] ?? 'Request failed', response.statusCode);
    }
  }
}
