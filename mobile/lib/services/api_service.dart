import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../core/constants/api_constants.dart';
import '../models/diagnosis_result.dart';

class ApiService {
  final http.Client client;

  ApiService({http.Client? client}) : client = client ?? http.Client();

  /// Uploads leaf image bytes for PyTorch CV classification & segmentation diagnosis
  Future<DiagnosisResult> diagnoseImage({
    required Uint8List imageBytes,
    required String filename,
    required String language,
  }) async {
    final uri = Uri.parse(ApiConstants.diagnoseEndpoint);
    final request = http.MultipartRequest('POST', uri);

    request.fields['lang'] = language;
    request.files.add(
      http.MultipartFile.fromBytes(
        'file',
        imageBytes,
        filename: filename,
      ),
    );

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      final jsonMap = jsonDecode(utf8.decode(response.bodyBytes));
      return DiagnosisResult.fromJson(jsonMap);
    } else {
      throw Exception('Diagnosis failed: ${response.body}');
    }
  }

  /// Sends user query to multi-lingual AI Plant Assistant
  Future<String> askAssistant(String message, String language) async {
    final uri = Uri.parse(ApiConstants.assistantEndpoint);
    final response = await client.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'message': message, 'language': language}),
    );

    if (response.statusCode == 200) {
      final jsonMap = jsonDecode(utf8.decode(response.bodyBytes));
      return jsonMap['response'] ?? '';
    } else {
      throw Exception('Assistant request failed');
    }
  }
}
