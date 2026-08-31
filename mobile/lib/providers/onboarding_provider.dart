import 'package:flutter/material.dart';
import '../services/storage_service.dart';

class OnboardingProvider extends ChangeNotifier {
  bool _isCompleted = false;
  bool _isInitialized = false;

  bool get isCompleted => _isCompleted;
  bool get isInitialized => _isInitialized;

  Future<void> init() async {
    final storage = await StorageService.getInstance();
    _isCompleted = storage.isOnboardingCompleted;
    _isInitialized = true;
    notifyListeners();
  }

  Future<void> completeOnboarding() async {
    final storage = await StorageService.getInstance();
    await storage.setOnboardingCompleted(true);
    _isCompleted = true;
    notifyListeners();
  }

  Future<void> resetOnboarding() async {
    final storage = await StorageService.getInstance();
    await storage.setOnboardingCompleted(false);
    _isCompleted = false;
    notifyListeners();
  }
}
