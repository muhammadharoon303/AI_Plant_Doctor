import '../core/network/api_client.dart';
import '../core/constants/app_constants.dart';
import '../models/disease_model.dart';
import '../models/plant_model.dart';

class PlantRepository {
  final ApiClient _apiClient;

  PlantRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  Future<List<DiseaseModel>> fetchDiseases({String? crop, String lang = 'en'}) async {
    String url = '${AppConstants.diseasesEndpoint}?lang=$lang';
    if (crop != null && crop.isNotEmpty) {
      url += '&crop=$crop';
    }
    final response = await _apiClient.get(url);
    final List items = response['items'] ?? [];
    return items.map((json) => DiseaseModel.fromJson(json)).toList();
  }

  Future<List<PlantModel>> fetchUserPlants(String token) async {
    final response = await _apiClient.get(
      AppConstants.plantsEndpoint,
      headers: {'Authorization': 'Bearer $token'},
    );
    final list = response['data'];
    if (list is List) {
      return list.map((json) => PlantModel.fromJson(Map<String, dynamic>.from(json))).toList();
    }
    return [];
  }

  Future<PlantModel> createPlant({
    required String token,
    required String name,
    required String cropType,
    String? variety,
    DateTime? plantingDate,
    String? location,
    String? notes,
  }) async {
    final response = await _apiClient.post(
      AppConstants.plantsEndpoint,
      headers: {'Authorization': 'Bearer $token'},
      body: {
        'name': name,
        'crop_type': cropType,
        'variety': variety,
        'planting_date': plantingDate?.toIso8601String(),
        'location': location,
        'notes': notes,
      },
    );
    return PlantModel.fromJson(response);
  }

  Future<PlantModel> updatePlant({
    required String token,
    required int plantId,
    String? name,
    String? cropType,
    String? variety,
    DateTime? plantingDate,
    String? location,
    String? notes,
  }) async {
    final response = await _apiClient.put(
      '${AppConstants.plantsEndpoint}/$plantId',
      headers: {'Authorization': 'Bearer $token'},
      body: {
        if (name != null) 'name': name,
        if (cropType != null) 'crop_type': cropType,
        if (variety != null) 'variety': variety,
        if (plantingDate != null) 'planting_date': plantingDate.toIso8601String(),
        if (location != null) 'location': location,
        if (notes != null) 'notes': notes,
      },
    );
    return PlantModel.fromJson(response);
  }

  Future<void> deletePlant({required String token, required int plantId}) async {
    await _apiClient.delete(
      '${AppConstants.plantsEndpoint}/$plantId',
      headers: {'Authorization': 'Bearer $token'},
    );
  }
}
