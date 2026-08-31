import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_ps.dart';
import 'app_localizations_ur.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'generated/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
      : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('ps'),
    Locale('ur')
  ];

  /// No description provided for @appTitle.
  ///
  /// In en, this message translates to:
  /// **'AI Plant Doctor'**
  String get appTitle;

  /// No description provided for @scannerTab.
  ///
  /// In en, this message translates to:
  /// **'Scanner'**
  String get scannerTab;

  /// No description provided for @historyTab.
  ///
  /// In en, this message translates to:
  /// **'History'**
  String get historyTab;

  /// No description provided for @knowledgeTab.
  ///
  /// In en, this message translates to:
  /// **'Knowledge Base'**
  String get knowledgeTab;

  /// No description provided for @assistantTab.
  ///
  /// In en, this message translates to:
  /// **'AI Assistant'**
  String get assistantTab;

  /// No description provided for @scanLeafTitle.
  ///
  /// In en, this message translates to:
  /// **'Diagnose Crop Health'**
  String get scanLeafTitle;

  /// No description provided for @scanLeafSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Take or upload a leaf photo to detect disease and estimate severity.'**
  String get scanLeafSubtitle;

  /// No description provided for @selectCamera.
  ///
  /// In en, this message translates to:
  /// **'Take Photo'**
  String get selectCamera;

  /// No description provided for @selectGallery.
  ///
  /// In en, this message translates to:
  /// **'Upload Image'**
  String get selectGallery;

  /// No description provided for @analyzingImage.
  ///
  /// In en, this message translates to:
  /// **'Analyzing leaf image with PyTorch AI...'**
  String get analyzingImage;

  /// No description provided for @diagnosisResult.
  ///
  /// In en, this message translates to:
  /// **'Diagnosis Report'**
  String get diagnosisResult;

  /// No description provided for @healthyPlant.
  ///
  /// In en, this message translates to:
  /// **'Healthy Plant'**
  String get healthyPlant;

  /// No description provided for @diseaseDetected.
  ///
  /// In en, this message translates to:
  /// **'Disease Detected'**
  String get diseaseDetected;

  /// No description provided for @severityLevel.
  ///
  /// In en, this message translates to:
  /// **'Severity Level'**
  String get severityLevel;

  /// No description provided for @affectedArea.
  ///
  /// In en, this message translates to:
  /// **'Infected Area'**
  String get affectedArea;

  /// No description provided for @viewOriginal.
  ///
  /// In en, this message translates to:
  /// **'Original Image'**
  String get viewOriginal;

  /// No description provided for @viewMask.
  ///
  /// In en, this message translates to:
  /// **'Lesion Segmentation Mask'**
  String get viewMask;

  /// No description provided for @biologicalTreatment.
  ///
  /// In en, this message translates to:
  /// **'Organic & Biological Treatment'**
  String get biologicalTreatment;

  /// No description provided for @chemicalTreatment.
  ///
  /// In en, this message translates to:
  /// **'Chemical Treatment'**
  String get chemicalTreatment;

  /// No description provided for @preventionTitle.
  ///
  /// In en, this message translates to:
  /// **'Prevention & Care'**
  String get preventionTitle;

  /// No description provided for @languageSelect.
  ///
  /// In en, this message translates to:
  /// **'Language'**
  String get languageSelect;

  /// No description provided for @english.
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get english;

  /// No description provided for @urdu.
  ///
  /// In en, this message translates to:
  /// **'Urdu (اردو)'**
  String get urdu;

  /// No description provided for @pashto.
  ///
  /// In en, this message translates to:
  /// **'Pashto (پښتو)'**
  String get pashto;

  /// No description provided for @askAssistantPlaceholder.
  ///
  /// In en, this message translates to:
  /// **'Ask AI Doctor about plant diseases...'**
  String get askAssistantPlaceholder;

  /// No description provided for @onboardingTitle1.
  ///
  /// In en, this message translates to:
  /// **'Plant Disease Detection'**
  String get onboardingTitle1;

  /// No description provided for @onboardingDesc1.
  ///
  /// In en, this message translates to:
  /// **'Diagnose crop diseases instantly with state-of-the-art PyTorch AI computer vision.'**
  String get onboardingDesc1;

  /// No description provided for @onboardingTitle2.
  ///
  /// In en, this message translates to:
  /// **'Camera Scanning'**
  String get onboardingTitle2;

  /// No description provided for @onboardingDesc2.
  ///
  /// In en, this message translates to:
  /// **'Take a photo of infected leaves to detect pathogens, lesions, and severity levels.'**
  String get onboardingDesc2;

  /// No description provided for @onboardingTitle3.
  ///
  /// In en, this message translates to:
  /// **'Plant Health Monitoring'**
  String get onboardingTitle3;

  /// No description provided for @onboardingDesc3.
  ///
  /// In en, this message translates to:
  /// **'Track disease progression over time and get localized organic and chemical treatment advice.'**
  String get onboardingDesc3;

  /// No description provided for @skip.
  ///
  /// In en, this message translates to:
  /// **'Skip'**
  String get skip;

  /// No description provided for @next.
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get next;

  /// No description provided for @getStarted.
  ///
  /// In en, this message translates to:
  /// **'Get Started'**
  String get getStarted;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'ps', 'ur'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'ps':
      return AppLocalizationsPs();
    case 'ur':
      return AppLocalizationsUr();
  }

  throw FlutterError(
      'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
      'an issue with the localizations generation tool. Please file an issue '
      'on GitHub with a reproducible sample app and the gen-l10n configuration '
      'that was used.');
}
