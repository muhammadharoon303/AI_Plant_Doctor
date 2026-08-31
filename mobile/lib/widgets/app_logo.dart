import 'package:flutter/material.dart';

class AppLogo extends StatelessWidget {
  final double size;
  final bool showTitle;

  const AppLogo({
    super.key,
    this.size = 96.0,
    this.showTitle = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(size * 0.25),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF1B4332).withValues(alpha: 0.35),
                blurRadius: 18,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(size * 0.25),
            child: Image.asset(
              'assets/images/app_icon.png',
              width: size,
              height: size,
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => Container(
                color: theme.colorScheme.primary,
                child: Icon(
                  Icons.eco,
                  size: size * 0.5,
                  color: Colors.white,
                ),
              ),
            ),
          ),
        ),
        if (showTitle) ...[
          const SizedBox(height: 16),
          Text(
            'AI Plant Doctor',
            style: theme.textTheme.headlineMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: theme.colorScheme.primary,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'AI-Powered Crop Care',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: Colors.grey[600],
              letterSpacing: 1.1,
            ),
          ),
        ],
      ],
    );
  }
}
