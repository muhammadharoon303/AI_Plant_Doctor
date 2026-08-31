import 'package:flutter/material.dart';
import '../../models/diagnosis_result.dart';
import '../custom_card.dart';

class RecentScansListWidget extends StatelessWidget {
  final List<DiagnosisResult> recentScans;
  final VoidCallback onStartScan;

  const RecentScansListWidget({
    super.key,
    required this.recentScans,
    required this.onStartScan,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Recent AI Diagnoses',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            if (recentScans.isNotEmpty)
              TextButton(
                onPressed: () {},
                child: const Text('View All'),
              ),
          ],
        ),
        const SizedBox(height: 8),

        if (recentScans.isEmpty)
          // Realistic Empty State
          CustomCard(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Icon(Icons.photo_filter_rounded, size: 48, color: Colors.grey[400]),
                  const SizedBox(height: 10),
                  Text(
                    'No AI Scan History Yet',
                    style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700]),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Capture or upload a leaf photo to get real PyTorch AI classification, U-Net lesion segmentation, and treatment advice.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                  ),
                  const SizedBox(height: 12),
                  ElevatedButton.icon(
                    onPressed: onStartScan,
                    icon: const Icon(Icons.camera_alt, size: 18),
                    label: const Text('Scan Leaf Now'),
                  ),
                ],
              ),
            ),
          )
        else
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: recentScans.length,
            itemBuilder: (context, index) {
              final scan = recentScans[index];
              return CustomCard(
                child: ListTile(
                  leading: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      scan.imageUrl,
                      width: 48,
                      height: 48,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => Container(
                        width: 48,
                        height: 48,
                        color: Colors.green[100],
                        child: const Icon(Icons.eco, color: Colors.green),
                      ),
                    ),
                  ),
                  title: Text(scan.diseaseName, style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text('${scan.cropName} • ${scan.severityStage} (${scan.affectedPercentage}%)'),
                  trailing: Chip(
                    label: Text('${(scan.confidence * 100).toStringAsFixed(0)}%'),
                    backgroundColor: Colors.green[50],
                  ),
                ),
              );
            },
          ),
      ],
    );
  }
}
