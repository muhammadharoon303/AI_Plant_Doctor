abstract class AppException implements Exception {
  final String message;
  final int? statusCode;

  AppException(this.message, [this.statusCode]);

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  NetworkException([String message = 'No internet connection or server unreachable'])
      : super(message);
}

class ApiException extends AppException {
  ApiException(String message, [int? statusCode]) : super(message, statusCode);
}

class AuthException extends AppException {
  AuthException([String message = 'Authentication failed. Please login again.'])
      : super(message, 401);
}

class ServerException extends AppException {
  ServerException([String message = 'Internal server error occurred'])
      : super(message, 500);
}
