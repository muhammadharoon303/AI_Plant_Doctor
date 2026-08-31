import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../../l10n/generated/app_localizations.dart';
import '../../../models/diagnosis_result.dart';
import '../../../services/api_service.dart';
import '../widgets/image_guidance_dialog.dart';
import '../widgets/image_preview_card.dart';
import 'diagnosis_result_screen.dart';

class ScannerScreen extends StatefulWidget {
  final String currentLanguage;
  const ScannerScreen({super.key, required this.currentLanguage});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  final ApiService _apiService = ApiService();
  final ImagePicker _picker = ImagePicker();

  Uint8List? _selectedBytes;
  String? _selectedFilename;
  bool _isLoading = false;
  bool _isCancelled = false;
  DiagnosisResult? _result;
  String? _errorMessage;

  void _showGuidanceAndPick(ImageSource source) {
    ImageGuidanceDialog.show(
      context,
      onContinue: () => _pickImage(source),
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? image = await _picker.pickImage(
        source: source,
        imageQuality: 85,
        maxWidth: 1024,
        maxHeight: 1024,
      );

      if (image != null) {
        final bytes = await image.readAsBytes();
        setState(() {
          _selectedBytes = bytes;
          _selectedFilename = image.name;
          _result = null;
          _errorMessage = null;
          _isCancelled = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = "Failed to pick image: $e";
      });
    }
  }

  Future<void> _diagnoseConfirmedImage() async {
    if (_selectedBytes == null || _selectedFilename == null) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _isCancelled = false;
    });

    try {
      final result = await _apiService.diagnoseImage(
        imageBytes: _selectedBytes!,
        filename: _selectedFilename!,
        language: widget.currentLanguage,
      );

      if (_isCancelled) return;

      setState(() {
        _result = result;
        _isLoading = false;
      });
    } catch (e) {
      if (_isCancelled) return;
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  void _cancelUpload() {
    setState(() {
      _isCancelled = true;
      _isLoading = false;
      _errorMessage = "Diagnosis analysis cancelled by user.";
    });
  }

  void _resetAll() {
    setState(() {
      _selectedBytes = null;
      _selectedFilename = null;
      _result = null;
      _errorMessage = null;
      _isLoading = false;
      _isCancelled = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_result != null) {
      return DiagnosisResultScreen(
        result: _result!,
        onRescan: _resetAll,
      );
    }

    final l10n = AppLocalizations.of(context)!;
    final theme = Theme.of(context);

    final bool isQualityError = _errorMessage != null &&
        (_errorMessage!.toLowerCase().contains("quality is insufficient") ||
         _errorMessage!.toLowerCase().contains("insufficient"));

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Header Card
          Card(
            color: theme.colorScheme.primaryContainer,
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  const Icon(Icons.center_focus_strong, size: 48, color: Colors.green),
                  const SizedBox(height: 8),
                  Text(
                    l10n.scanLeafTitle,
                    style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    l10n.scanLeafSubtitle,
                    style: theme.textTheme.bodyMedium,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Camera & Gallery Source Selection Buttons
          if (_selectedBytes == null) ...[
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => _showGuidanceAndPick(ImageSource.camera),
                    icon: const Icon(Icons.camera_alt),
                    label: Text(l10n.selectCamera),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => _showGuidanceAndPick(ImageSource.gallery),
                    icon: const Icon(Icons.photo_library),
                    label: Text(l10n.selectGallery),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Center(
              child: TextButton.icon(
                onPressed: () => ImageGuidanceDialog.show(context, onContinue: () {}),
                icon: const Icon(Icons.lightbulb_outline, size: 18),
                label: const Text('View Photo Quality Guidelines'),
              ),
            ),
          ],

          // Image Preview Card (Before Confirming Analysis)
          if (_selectedBytes != null) ...[
            ImagePreviewCard(
              imageBytes: _selectedBytes!,
              filename: _selectedFilename ?? 'leaf_image.jpg',
              onRetake: _resetAll,
              onConfirm: _diagnoseConfirmedImage,
              isLoading: _isLoading,
              onCancel: _cancelUpload,
            ),
            const SizedBox(height: 16),
          ],

          // Image Quality Warning Container
          if (isQualityError) ...[
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.amber.shade50,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.amber.shade400, width: 1.5),
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      Icon(Icons.warning_amber_rounded, color: Colors.amber.shade900, size: 28),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          "Image quality is insufficient. Please capture another image.",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                            color: Colors.amber.shade900,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    _errorMessage!.replaceAll("Exception:", "").trim(),
                    style: TextStyle(fontSize: 12, color: Colors.amber.shade900),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () => _showGuidanceAndPick(ImageSource.camera),
                      icon: const Icon(Icons.camera_alt),
                      label: const Text('Retake Photo'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.amber.shade800,
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
          ] else if (_errorMessage != null) ...[
            // General Error Message Alert Box
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.red[50],
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.red.shade200),
              ),
              child: Row(
                children: [
                  const Icon(Icons.error_outline, color: Colors.red),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      _errorMessage!.replaceAll("Exception:", "").trim(),
                      style: const TextStyle(color: Colors.red, fontSize: 13),
                    ),
                  ),
                  TextButton(
                    onPressed: _resetAll,
                    child: const Text('Try Again'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
          ],
        ],
      ),
    );
  }
}
