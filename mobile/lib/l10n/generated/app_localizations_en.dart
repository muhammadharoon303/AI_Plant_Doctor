// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'AI Plant Doctor';

  @override
  String get scannerTab => 'Scanner';

  @override
  String get historyTab => 'History';

  @override
  String get knowledgeTab => 'Knowledge Base';

  @override
  String get assistantTab => 'AI Assistant';

  @override
  String get scanLeafTitle => 'Diagnose Crop Health';

  @override
  String get scanLeafSubtitle =>
      'Take or upload a leaf photo to detect disease and estimate severity.';

  @override
  String get selectCamera => 'Take Photo';

  @override
  String get selectGallery => 'Upload Image';

  @override
  String get analyzingImage => 'Analyzing leaf image with PyTorch AI...';

  @override
  String get diagnosisResult => 'Diagnosis Report';

  @override
  String get healthyPlant => 'Healthy Plant';

  @override
  String get diseaseDetected => 'Disease Detected';

  @override
  String get severityLevel => 'Severity Level';

  @override
  String get affectedArea => 'Infected Area';

  @override
  String get viewOriginal => 'Original Image';

  @override
  String get viewMask => 'Lesion Segmentation Mask';

  @override
  String get biologicalTreatment => 'Organic & Biological Treatment';

  @override
  String get chemicalTreatment => 'Chemical Treatment';

  @override
  String get preventionTitle => 'Prevention & Care';

  @override
  String get languageSelect => 'Language';

  @override
  String get english => 'English';

  @override
  String get urdu => 'Urdu (اردو)';

  @override
  String get pashto => 'Pashto (پښتو)';

  @override
  String get askAssistantPlaceholder => 'Ask AI Doctor about plant diseases...';

  @override
  String get onboardingTitle1 => 'Plant Disease Detection';

  @override
  String get onboardingDesc1 =>
      'Diagnose crop diseases instantly with state-of-the-art PyTorch AI computer vision.';

  @override
  String get onboardingTitle2 => 'Camera Scanning';

  @override
  String get onboardingDesc2 =>
      'Take a photo of infected leaves to detect pathogens, lesions, and severity levels.';

  @override
  String get onboardingTitle3 => 'Plant Health Monitoring';

  @override
  String get onboardingDesc3 =>
      'Track disease progression over time and get localized organic and chemical treatment advice.';

  @override
  String get skip => 'Skip';

  @override
  String get next => 'Next';

  @override
  String get getStarted => 'Get Started';
}
