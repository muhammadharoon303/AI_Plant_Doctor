import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../../models/history_item_model.dart';
import '../../../../widgets/custom_card.dart';

class BeforeAfterComparisonWidget extends StatelessWidget {
  final HistoryItemModel previousScan;
  final HistoryItemModel latestScan;

  const BeforeAfterComparisonWidget({
    super.key,
    required this.previousScan,
    required this.latestScan,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final double deltaArea = latestScan.affectedPercentage - previousScan.affectedPercentage;
    final String deltaSign = deltaArea > 0 ? '+' : '';
    final String deltaText = '$deltaSign${deltaArea.toStringAsFixed(1)}%';

    Color deltaColor = Colors.blue.shade800;
    IconData deltaIcon = Icons.trending_flat;

    if (deltaArea < -2.5) {
      deltaColor = Colors.green.shade800;
      deltaIcon = Icons.trending_down;
    } else if (deltaArea > 2.5) {
      deltaColor = Colors.red.shade800;
      deltaIcon = Icons.trending_up;
    }

    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.compare_arrows, color: theme.colorScheme.primary, size: 20),
                  const SizedBox(width: 8),
                  Text(
                    'BEFORE / AFTER SCAN COMPARISON',
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
                  color: deltaColor.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  children: [
                    Icon(deltaIcon, size: 14, color: deltaColor),
                    const SizedBox(width: 4),
                    Text(
                      'Diff: $deltaText',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: deltaColor),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Side-by-Side Images & Metrics
          Row(
            children: [
              Expanded(
                child: _ScanSideCard(
                  label: 'BEFORE',
                  scan: previousScan,
                  badgeColor: Colors.grey.shade700,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _ScanSideCard(
                  label: 'AFTER (LATEST)',
                  scan: latestScan,
                  badgeColor: Colors.green.shade800,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ScanSideCard extends StatelessWidget {
  final String label;
  final HistoryItemModel scan;
  final Color badgeColor;

  const _ScanSideCard({
    required this.label,
    required this.scan,
    required this.badgeColor,
  });

  @override
  Widget build(BuildContext context) {
    final dateStr = DateFormat('MMM d, yyyy').format(scan.createdAt);
    final double confPct = scan.confidence <= 1.0 ? scan.confidence * 100.0 : scan.confidence;

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade300),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: badgeColor,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              label,
              style: const TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(height: 8),

          // Image Thumbnail
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Container(
              width: double.infinity,
              height: 90,
              color: Colors.grey.shade300,
              child: scan.imageUrl.isNotEmpty
                  ? Image.network(
                      scan.imageUrl,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => const Icon(Icons.eco, color: Colors.green, size: 36),
                    )
                  : const Icon(Icons.eco, color: Colors.green, size: 36),
            ),
          ),
          const SizedBox(height: 8),

          Text(
            scan.diseaseName,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          Text(
            'Lesion Coverage: ${scan.affectedPercentage.toStringAsFixed(1)}%',
            style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
          ),
          Text(
            'Stage: ${scan.severityStage} (${confPct.toStringAsFixed(0)}%)',
            style: const TextStyle(fontSize: 10, color: Colors.grey),
          ),
          const SizedBox(height: 2),
          Text(
            dateStr,
            style: TextStyle(fontSize: 9, color: Colors.grey.shade600),
          ),
        ],
      ),
    );
  }
}
