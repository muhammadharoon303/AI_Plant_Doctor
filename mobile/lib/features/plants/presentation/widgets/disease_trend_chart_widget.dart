import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../../models/history_item_model.dart';
import '../../../../widgets/custom_card.dart';

class DiseaseTrendChartWidget extends StatelessWidget {
  final List<HistoryItemModel> scans;

  const DiseaseTrendChartWidget({super.key, required this.scans});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    if (scans.isEmpty) {
      return const SizedBox.shrink();
    }

    // Chronological order (oldest to newest for progression chart)
    final sortedScans = List<HistoryItemModel>.from(scans.reversed);
    final double maxCoverage = sortedScans.map((s) => s.affectedPercentage).reduce((a, b) => a > b ? a : b);
    final double ceilMax = (maxCoverage <= 0.0) ? 20.0 : (maxCoverage > 80 ? 100.0 : maxCoverage + 15.0);

    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.show_chart, color: theme.colorScheme.primary, size: 20),
              const SizedBox(width: 8),
              Text(
                'LESION COVERAGE TREND OVER TIME (%)',
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.5,
                  color: theme.colorScheme.primary,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Visual Custom Paint Bar Chart Widget
          SizedBox(
            height: 130,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: sortedScans.map((scan) {
                final double heightRatio = (scan.affectedPercentage / ceilMax).clamp(0.05, 1.0);
                final dateLabel = DateFormat('MMM d').format(scan.createdAt);
                final bool isHealthy = scan.diseaseName.toLowerCase().contains('healthy');

                return Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Text(
                      '${scan.affectedPercentage.toStringAsFixed(1)}%',
                      style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Container(
                      width: 24,
                      height: 80 * heightRatio,
                      decoration: BoxDecoration(
                        color: isHealthy
                            ? Colors.green.shade600
                            : (scan.affectedPercentage > 20 ? Colors.red.shade600 : Colors.orange.shade600),
                        borderRadius: const BorderRadius.vertical(top: Radius.circular(6)),
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      dateLabel,
                      style: TextStyle(fontSize: 9, color: Colors.grey.shade700),
                    ),
                  ],
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 8),

          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _LegendDot(color: Colors.green.shade600, label: 'Healthy'),
              const SizedBox(width: 12),
              _LegendDot(color: Colors.orange.shade600, label: 'Mild/Moderate'),
              const SizedBox(width: 12),
              _LegendDot(color: Colors.red.shade600, label: 'Severe (>20%)'),
            ],
          ),
        ],
      ),
    );
  }
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;

  const _LegendDot({required this.color, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
      ],
    );
  }
}
