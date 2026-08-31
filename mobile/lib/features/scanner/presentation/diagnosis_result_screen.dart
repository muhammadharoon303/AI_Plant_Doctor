import 'package:flutter/material.dart';
import '../../../models/diagnosis_result.dart';
import '../widgets/segmentation_overlay_widget.dart';
import '../../../../widgets/custom_card.dart';

class DiagnosisResultScreen extends StatelessWidget {
  final DiagnosisResult result;
  final VoidCallback onRescan;

  const DiagnosisResultScreen({
    super.key,
    required this.result,
    required this.onRescan,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final double confidencePct = result.confidence <= 1.0 ? result.confidence * 100.0 : result.confidence;
    final bool isLowConfidence = confidencePct < 60.0;

    String confidenceBadgeText = 'High Confidence';
    Color confidenceBadgeColor = Colors.green.shade700;
    Color confidenceBgColor = Colors.green.shade50;

    if (confidencePct < 60.0) {
      confidenceBadgeText = 'Low Confidence';
      confidenceBadgeColor = Colors.amber.shade900;
      confidenceBgColor = Colors.amber.shade50;
    } else if (confidencePct < 75.0) {
      confidenceBadgeText = 'Moderate Confidence';
      confidenceBadgeColor = Colors.blue.shade900;
      confidenceBgColor = Colors.blue.shade50;
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis Report'),
        actions: [
          IconButton(
            icon: const Icon(Icons.center_focus_strong),
            onPressed: onRescan,
            tooltip: 'Scan Another Leaf',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // LOW CONFIDENCE WARNING BANNER
            if (isLowConfidence) ...[
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.amber.shade100,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.amber.shade700, width: 1.5),
                ),
                child: Row(
                  children: [
                    Icon(Icons.warning_amber_rounded, color: Colors.amber.shade900, size: 32),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Low-confidence result. Please capture a clearer image or seek expert confirmation.',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 13,
                              color: Colors.amber.shade900,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'The AI confidence is ${confidencePct.toStringAsFixed(1)}%. Predictions below 60% are not guaranteed.',
                            style: TextStyle(fontSize: 11, color: Colors.amber.shade900),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
            ],

            // SECTION 1: AI PREDICTION (SCREENING RESULT)
            CustomCard(
              color: theme.colorScheme.surface,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.smart_toy_outlined, color: theme.colorScheme.primary, size: 20),
                          const SizedBox(width: 8),
                          Text(
                            'AI COMPUTER VISION PREDICTION',
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
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade200,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          result.modelVersion,
                          style: TextStyle(fontSize: 10, color: Colors.grey.shade800),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Image Preview & U-Net Segmentation Mask
                  SegmentationOverlayWidget(
                    imageUrl: result.imageUrl,
                    maskUrl: result.maskUrl,
                  ),
                  const SizedBox(height: 16),

                  // Crop & Disease Name Header
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Crop: ${result.cropName}',
                              style: TextStyle(fontSize: 12, color: Colors.grey.shade700, fontWeight: FontWeight.bold),
                            ),
                            Text(
                              result.diseaseName,
                              style: TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.bold,
                                color: result.isHealthy ? Colors.green.shade800 : Colors.red.shade800,
                              ),
                            ),
                            if (result.scientificName != null && result.scientificName!.isNotEmpty)
                              Text(
                                result.scientificName!,
                                style: const TextStyle(fontStyle: FontStyle.italic, fontSize: 13, color: Colors.grey),
                              ),
                          ],
                        ),
                      ),
                      // Confidence Badge
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: confidenceBgColor,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: confidenceBadgeColor.withValues(alpha: 0.3)),
                        ),
                        child: Column(
                          children: [
                            Text(
                              '${confidencePct.toStringAsFixed(1)}%',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                                color: confidenceBadgeColor,
                              ),
                            ),
                            Text(
                              confidenceBadgeText,
                              style: TextStyle(fontSize: 10, color: confidenceBadgeColor),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Lesion Severity Bar
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Lesion Coverage: ${result.affectedPercentage.toStringAsFixed(1)}%',
                        style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
                      ),
                      Chip(
                        label: Text(result.severityStage),
                        backgroundColor: result.isHealthy ? Colors.green.shade100 : Colors.orange.shade100,
                        visualDensity: VisualDensity.compact,
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: LinearProgressIndicator(
                      value: (result.affectedPercentage / 100.0).clamp(0.0, 1.0),
                      minHeight: 8,
                      backgroundColor: Colors.grey.shade200,
                      color: result.affectedPercentage > 20 ? Colors.red : Colors.orange,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Icon(Icons.info_outline, size: 14, color: Colors.grey.shade700),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          'Severity level is an image-based visual estimate from leaf surface analysis. For precise field staging, consult an agricultural extension specialist.',
                          style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // SECTION DIVIDER: VERIFIED KNOWLEDGE
            Row(
              children: [
                const Expanded(child: Divider()),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 12.0),
                  child: Row(
                    children: [
                      Icon(Icons.verified, color: Colors.green.shade700, size: 18),
                      const SizedBox(width: 6),
                      Text(
                        'VERIFIED AGRICULTURAL KNOWLEDGE',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 0.6,
                          color: Colors.green.shade800,
                        ),
                      ),
                    ],
                  ),
                ),
                const Expanded(child: Divider()),
              ],
            ),
            const SizedBox(height: 16),

            // SECTION 2: VERIFIED KNOWLEDGE CARDS
            // 1. Symptoms Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.sick_outlined, color: Colors.orange.shade800, size: 22),
                      const SizedBox(width: 10),
                      Text(
                        'Symptoms',
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    result.symptoms.isNotEmpty ? result.symptoms : result.description,
                    style: const TextStyle(fontSize: 14, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 2. Possible Causes Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.biotech_outlined, color: Colors.purple.shade700, size: 22),
                      const SizedBox(width: 10),
                      Text(
                        'Possible Causes & Pathogens',
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    result.possibleCauses,
                    style: const TextStyle(fontSize: 14, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 3. Management & Cultivation Guidance Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.shield_outlined, color: Colors.green.shade800, size: 22),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'Management & Cultivation Guidance',
                          style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  if (result.management.isNotEmpty) ...[
                    Text(
                      'Management Recommendations:',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey.shade800),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      result.management,
                      style: const TextStyle(fontSize: 14, height: 1.4),
                    ),
                    const SizedBox(height: 10),
                  ],
                  if (result.prevention.isNotEmpty) ...[
                    Text(
                      'Cultural & Care Prevention:',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey.shade800),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      result.prevention,
                      style: const TextStyle(fontSize: 14, height: 1.4),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 4. Treatment Options Card (Biological & Chemical)
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.medication_liquid_outlined, color: Colors.blue.shade800, size: 22),
                      const SizedBox(width: 10),
                      Text(
                        'Recommended Treatments',
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  
                  // Biological / Organic Treatment
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.green.shade200),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.eco, color: Colors.green.shade800, size: 18),
                            const SizedBox(width: 6),
                            Text(
                              'Organic & Biological Treatment',
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.green.shade900),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          result.biologicalTreatment.isNotEmpty ? result.biologicalTreatment : 'Maintain balanced nutrition and neem oil application.',
                          style: TextStyle(fontSize: 13, color: Colors.green.shade900, height: 1.3),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 10),

                  // Chemical Treatment
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.blue.shade200),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.science, color: Colors.blue.shade800, size: 18),
                            const SizedBox(width: 6),
                            Text(
                              'Chemical Protectants',
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.blue.shade900),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          result.chemicalTreatment.isNotEmpty ? result.chemicalTreatment : 'Apply registered protective copper or chlorothalonil fungicides.',
                          style: TextStyle(fontSize: 13, color: Colors.blue.shade900, height: 1.3),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 5. Safety Information & Pre-Harvest Interval Card
            CustomCard(
              color: Colors.red.shade50,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.health_and_safety_outlined, color: Colors.red.shade900, size: 22),
                      const SizedBox(width: 10),
                      Text(
                        'Safety & Harvest Guidelines',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Colors.red.shade900,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    result.safetyInformation,
                    style: TextStyle(fontSize: 13, color: Colors.red.shade900, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 6. Agricultural Sources & References Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.menu_book_outlined, color: Colors.grey.shade800, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        'Verified Sources & References',
                        style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ...result.sources.map((src) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2.0),
                    child: Row(
                      children: [
                        const Icon(Icons.check_circle_outline, size: 14, color: Colors.green),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            src,
                            style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
                          ),
                        ),
                      ],
                    ),
                  )),
                ],
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
