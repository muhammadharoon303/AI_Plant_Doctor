import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocaleProvider extends ChangeNotifier {
  static const String _prefKey = 'user_language_preference';
  Locale _locale = const Locale('en');

  LocaleProvider() {
    _loadSavedLocale();
  }

  Locale get locale => _locale;
  String get languageCode => _locale.languageCode;
  bool get isRtl => _locale.languageCode == 'ur' || _locale.languageCode == 'ps';

  Future<void> _loadSavedLocale() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedLang = prefs.getString(_prefKey);
      if (savedLang != null && ['en', 'ur', 'ps'].contains(savedLang)) {
        _locale = Locale(savedLang);
        notifyListeners();
      }
    } catch (_) {}
  }

  Future<void> setLocale(Locale newLocale) async {
    if (_locale != newLocale && ['en', 'ur', 'ps'].contains(newLocale.languageCode)) {
      _locale = newLocale;
      notifyListeners();
      try {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_prefKey, newLocale.languageCode);
      } catch (_) {}
    }
  }

  Future<void> setLanguageCode(String langCode) async {
    await setLocale(Locale(langCode));
  }
}
