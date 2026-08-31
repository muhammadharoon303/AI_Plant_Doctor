import 'package:flutter/material.dart';
import '../custom_card.dart';

class HealthSummaryCardWidget extends StatelessWidget {
  final int totalScans;
  final double healthyPercentage;
  final int activeAlertsCount;

  const HealthSummaryCardWidget({
    super.key,
    this.totalScans = 0,
    this.healthyPercentage = 100.0,
    this.activeAlertsCount = 1,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return CustomCard(
      elevation: 3,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Plant Health Overview',
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              Icon(Icons.insights, color: theme.colorScheme.primary),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              _MetricTile(
                icon: Icons.qr_code_scanner,
                color: Colors.blue,
                value: '$totalScans',
                label: 'Scans Done',
              ),
              _MetricTile(
                icon: Icons.health_and_safety,
                color: Colors.green,
                value: '${healthyPercentage.toStringAsFixed(0)}%',
                label: 'Healthy Ratio',
              ),
              _MetricTile(
                icon: Icons.warning_amber_rounded,
                color: Colors.orange,
                value: '$activeAlertsCount',
                label: 'Active Alerts',
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _MetricTile extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String value;
  final String label;

  const _MetricTile({
    required this.icon,
    required this.color,
    required this.value,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4),
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withValues(alpha: 0.2)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 6),
            Text(
              value,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                color: Colors.grey[700],
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
