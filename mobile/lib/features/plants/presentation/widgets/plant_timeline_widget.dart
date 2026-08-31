import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import '../../../../core/constants/api_constants.dart';
import '../../../../models/history_item_model.dart';
import '../../../../models/diagnosis_result.dart';
import '../../../../widgets/custom_card.dart';
import '../../../scanner/presentation/diagnosis_result_screen.dart';
import 'before_after_comparison_widget.dart';
import 'disease_trend_chart_widget.dart';

class PlantTimelineWidget extends StatefulWidget {
  final int plantId;

  const PlantTimelineWidget({super.key, required this.plantId});

  @override
  State<PlantTimelineWidget> createState() => _PlantTimelineWidgetState();
}

class _PlantTimelineWidgetState extends State<PlantTimelineWidget> {
  bool _isLoading = true;
  String? _errorMessage;

  List<HistoryItemModel> _scans = [];
  Map<String, dynamic>? _progressData;

  @override
  void initState() {
    super.initState();
    _fetchTimelineData();
  }

  String get _rootBaseUrl {
    return ApiConstants.baseUrl.replaceAll('/api/v1', '');
  }

  Future<void> _fetchTimelineData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final scansUri = Uri.parse('$_rootBaseUrl/api/plants/${widget.plantId}/scans');
      final progressUri = Uri.parse('$_rootBaseUrl/api/plants/${widget.plantId}/progress');

      final scansRes = await http.get(scansUri);
      final progressRes = await http.get(progressUri);

      if (scansRes.statusCode == 200 && progressRes.statusCode == 200) {
        final scansJson = json.decode(scansRes.body);
        final progressJson = json.decode(progressRes.body);

        final List items = scansJson['items'] ?? [];
        setState(() {
          _scans = items.map((x) => HistoryItemModel.fromJson(x)).toList();
          _progressData = progressJson;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Failed to load timeline data.';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Network error loading timeline: $e';
        _isLoading = false;
      });
    }
  }

  void _openScanDetail(HistoryItemModel item) {
    final double conf = item.confidence <= 1.0 ? item.confidence : item.confidence / 100.0;
    final bool isHealthy = item.diseaseName.toLowerCase().contains('healthy');

    final result = DiagnosisResult(
      scanId: item.scanId,
      diseaseKey: item.diseaseKey,
      cropName: item.cropName,
      diseaseName: item.diseaseName,
      confidence: conf,
      modelVersion: item.modelVersion,
      affectedPercentage: item.affectedPercentage,
      severityStage: item.severityStage,
      isHealthy: isHealthy,
      imageUrl: item.imageUrl,
      maskUrl: item.maskUrl,
      description: 'Historical plant monitoring record for ${item.cropName}.',
      symptoms: 'Observed leaf surface symptoms: ${item.diseaseName}.',
      biologicalTreatment: 'Apply organic bio-fungicides and neem oil spray.',
      chemicalTreatment: 'Use registered protective crop sprays as per extension advice.',
      prevention: 'Ensure balanced fertilization, drainage, and field sanitation.',
      createdAt: item.createdAt,
    );

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => DiagnosisResultScreen(
          result: result,
          onRescan: () => Navigator.pop(context),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    if (_isLoading) {
      return const Padding(
        padding: EdgeInsets.all(24.0),
        child: Center(child: CircularProgressIndicator()),
      );
    }

    if (_errorMessage != null) {
      return CustomCard(
        child: Column(
          children: [
            Text(_errorMessage!, style: const TextStyle(color: Colors.red, fontSize: 13)),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _fetchTimelineData,
              child: const Text('Retry Loading Timeline'),
            ),
          ],
        ),
      );
    }

    if (_scans.isEmpty) {
      return CustomCard(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Icon(Icons.center_focus_weak, size: 48, color: Colors.grey.shade400),
              const SizedBox(height: 8),
              Text(
                'No monitoring scans linked to this plant profile yet.',
                style: TextStyle(color: Colors.grey.shade700, fontSize: 14),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              const Text(
                'Scan a leaf image to track disease progression over time.',
                style: TextStyle(color: Colors.grey, fontSize: 12),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
    }

    final trend = _progressData?['health_trend'] ?? 'Stable';
    Color trendColor = Colors.blue.shade800;
    IconData trendIcon = Icons.trending_flat;

    if (trend == 'Improving') {
      trendColor = Colors.green.shade800;
      trendIcon = Icons.trending_down; // Affected area decreased
    } else if (trend == 'Worsening') {
      trendColor = Colors.red.shade800;
      trendIcon = Icons.trending_up; // Affected area increased
    }

    final latestScan = _scans.isNotEmpty ? _scans[0] : null;
    final previousScan = _scans.length > 1 ? _scans[1] : null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Health Progress & Trend Summary Card
        CustomCard(
          color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(Icons.analytics_outlined, color: theme.colorScheme.primary, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        'PLANT HEALTH PROGRESSION',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 0.5,
                          color: theme.colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: trendColor.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      children: [
                        Icon(trendIcon, size: 16, color: trendColor),
                        const SizedBox(width: 4),
                        Text(
                          'Trend: $trend',
                          style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: trendColor),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Previous Scan vs Latest Scan Comparison Card
              if (previousScan != null && latestScan != null) ...[
                BeforeAfterComparisonWidget(
                  previousScan: previousScan,
                  latestScan: latestScan,
                ),
                const SizedBox(height: 12),
              ],

              Text(
                'Total Scans: ${_scans.length} monitoring observations recorded.',
                style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // Disease Trend Line/Bar Chart
        if (_scans.length >= 2) ...[
          DiseaseTrendChartWidget(scans: _scans),
          const SizedBox(height: 16),
        ],
        const SizedBox(height: 16),

        // Scan Timeline List Header
        Text(
          'Chronological Scan Timeline',
          style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),

        // Timeline Items
        ..._scans.map((scan) {
          final dateStr = DateFormat('MMM d, yyyy • h:mm a').format(scan.createdAt);
          final double confPct = scan.confidence <= 1.0 ? scan.confidence * 100.0 : scan.confidence;
          final bool isHealthy = scan.diseaseName.toLowerCase().contains('healthy');

          return Padding(
            padding: const EdgeInsets.only(bottom: 10.0),
            child: CustomCard(
              onTap: () => _openScanDetail(scan),
              child: Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      width: 56,
                      height: 56,
                      color: Colors.grey.shade200,
                      child: scan.imageUrl.isNotEmpty
                          ? Image.network(
                              scan.imageUrl,
                              fit: BoxFit.cover,
                              errorBuilder: (_, __, ___) => const Icon(Icons.eco, color: Colors.green),
                            )
                          : const Icon(Icons.eco, color: Colors.green),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              scan.diseaseName,
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                            ),
                            Chip(
                              label: Text(scan.severityStage),
                              backgroundColor: isHealthy ? Colors.green.shade100 : Colors.orange.shade100,
                              visualDensity: VisualDensity.compact,
                              labelStyle: const TextStyle(fontSize: 9),
                            ),
                          ],
                        ),
                        Text(
                          'Coverage: ${scan.affectedPercentage.toStringAsFixed(1)}% | Conf: ${confPct.toStringAsFixed(1)}%',
                          style: TextStyle(fontSize: 11, color: Colors.grey.shade700),
                        ),
                        const SizedBox(height: 2),
                        Text(dateStr, style: TextStyle(fontSize: 10, color: Colors.grey.shade600)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          );
        }),
      ],
    );
  }
}
