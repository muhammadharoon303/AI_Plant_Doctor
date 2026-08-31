import 'package:flutter/material.dart';
import '../custom_card.dart';

class MonitoringRemindersWidget extends StatelessWidget {
  const MonitoringRemindersWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final reminders = [
      {
        'title': 'Weekly Leaf Inspection',
        'subtitle': 'Inspect tomato plants for early blight symptoms',
        'time': 'Today, 5:00 PM',
        'icon': Icons.search,
        'color': Colors.green,
      },
      {
        'title': 'Organic Neem Spray',
        'subtitle': 'Apply preventive bio-pesticide spray',
        'time': 'Tomorrow, 8:00 AM',
        'icon': Icons.water_drop,
        'color': Colors.blue,
      },
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Monitoring Reminders',
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        ...reminders.map(
          (item) => CustomCard(
            child: ListTile(
              contentPadding: EdgeInsets.zero,
              leading: Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: (item['color'] as Color).withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(item['icon'] as IconData, color: item['color'] as Color),
              ),
              title: Text(
                item['title'] as String,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
              ),
              subtitle: Text(item['subtitle'] as String, style: const TextStyle(fontSize: 12)),
              trailing: Text(
                item['time'] as String,
                style: TextStyle(fontSize: 11, color: theme.colorScheme.primary, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
