import 'package:flutter/material.dart';
import '../models/disease_model.dart';
import '../models/plant_model.dart';
import '../repositories/plant_repository.dart';

class PlantProvider extends ChangeNotifier {
  final PlantRepository _repository;

  PlantProvider({PlantRepository? repository})
      : _repository = repository ?? PlantRepository();

  List<DiseaseModel> _diseases = [];
  List<PlantModel> _userPlants = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<DiseaseModel> get diseases => _diseases;
  List<PlantModel> get userPlants => _userPlants;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  Future<void> loadDiseases({String? crop, String lang = 'en'}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _diseases = await _repository.fetchDiseases(crop: crop, lang: lang);
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadUserPlants(String token) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _userPlants = await _repository.fetchUserPlants(token);
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createPlant({
    required String token,
    required String name,
    required String cropType,
    String? variety,
    DateTime? plantingDate,
    String? location,
    String? notes,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final newPlant = await _repository.createPlant(
        token: token,
        name: name,
        cropType: cropType,
        variety: variety,
        plantingDate: plantingDate,
        location: location,
        notes: notes,
      );
      _userPlants.insert(0, newPlant);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> updatePlant({
    required String token,
    required int plantId,
    String? name,
    String? cropType,
    String? variety,
    DateTime? plantingDate,
    String? location,
    String? notes,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final updated = await _repository.updatePlant(
        token: token,
        plantId: plantId,
        name: name,
        cropType: cropType,
        variety: variety,
        plantingDate: plantingDate,
        location: location,
        notes: notes,
      );
      final idx = _userPlants.indexWhere((p) => p.id == plantId);
      if (idx != -1) {
        _userPlants[idx] = updated;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> deletePlant({required String token, required int plantId}) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _repository.deletePlant(token: token, plantId: plantId);
      _userPlants.removeWhere((p) => p.id == plantId);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
}
