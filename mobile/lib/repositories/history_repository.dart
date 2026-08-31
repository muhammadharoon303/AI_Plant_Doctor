import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants/api_constants.dart';
import '../models/history_item_model.dart';

class HistoryRepository {
  final http.Client _client;

  HistoryRepository({http.Client? client}) : _client = client ?? http.Client();

  String get _rootBaseUrl {
    final base = ApiConstants.baseUrl;
    return base.replaceAll('/api/v1', '');
  }

  Future<List<HistoryItemModel>> getDiagnosisHistory({
    String? crop,
    String? disease,
    String? searchQuery,
  }) async {
    final queryParams = <String, String>{};
    if (crop != null && crop.isNotEmpty) queryParams['crop'] = crop;
    if (disease != null && disease.isNotEmpty) queryParams['disease'] = disease;
    if (searchQuery != null && searchQuery.isNotEmpty) queryParams['q'] = searchQuery;

    final uri = Uri.parse('$_rootBaseUrl/api/diagnosis/history').replace(queryParameters: queryParams);

    try {
      final response = await _client.get(uri);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List items = data['items'] ?? [];
        return items.map((jsonItem) => HistoryItemModel.fromJson(jsonItem)).toList();
      } else {
        throw Exception('Failed to fetch diagnosis history: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error fetching history: $e');
    }
  }

  Future<HistoryItemModel> getHistoryItemDetail(int id) async {
    final uri = Uri.parse('$_rootBaseUrl/api/diagnosis/$id');
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return HistoryItemModel.fromJson(data);
    } else {
      throw Exception('Failed to load diagnosis scan detail #$id');
    }
  }
}
