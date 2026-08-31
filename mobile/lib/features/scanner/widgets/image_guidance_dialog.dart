import 'package:flutter/material.dart';

class ImageGuidanceDialog extends StatelessWidget {
  final VoidCallback onContinue;

  const ImageGuidanceDialog({
    super.key,
    required this.onContinue,
  });

  static void show(BuildContext context, {required VoidCallback onContinue}) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (_) => ImageGuidanceDialog(onContinue: onContinue),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: theme.colorScheme.primaryContainer,
                  shape: BoxShape.circle,
                ),
                child: Icon(Icons.lightbulb_rounded, color: theme.colorScheme.primary),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  'Photo Quality Guidance',
                  style: theme.textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text(
            'To get accurate PyTorch AI diagnosis & lesion mask segmentation, follow these tips:',
            style: TextStyle(color: Colors.grey, fontSize: 14),
          ),
          const SizedBox(height: 16),

          const _GuidanceTipRow(
            icon: Icons.filter_center_focus,
            color: Colors.green,
            title: 'Use a clear leaf image',
            subtitle: 'Ensure the infected leaf or lesion is sharp and in clear focus.',
          ),
          const _GuidanceTipRow(
            icon: Icons.blur_off,
            color: Colors.orange,
            title: 'Avoid extreme blur',
            subtitle: 'Hold camera steady to avoid motion blur or out-of-focus shots.',
          ),
          const _GuidanceTipRow(
            icon: Icons.wb_sunny,
            color: Colors.amber,
            title: 'Ensure sufficient lighting',
            subtitle: 'Take photos in natural daylight or well-lit environments.',
          ),
          const _GuidanceTipRow(
            icon: Icons.center_focus_strong,
            color: Colors.blue,
            title: 'Keep leaf fully visible',
            subtitle: 'Fill the camera frame with the affected plant leaf tissue.',
          ),

          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              onContinue();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: theme.colorScheme.primary,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: const Text(
              'Got It, Let\'s Capture',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }
}

class _GuidanceTipRow extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String title;
  final String subtitle;

  const _GuidanceTipRow({
    required this.icon,
    required this.color,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: color, size: 22),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
                Text(
                  subtitle,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
