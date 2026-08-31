import 'package:flutter/material.dart';

class NotificationSettingsDialog extends StatefulWidget {
  const NotificationSettingsDialog({super.key});

  static Future<void> show(BuildContext context) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => const NotificationSettingsDialog(),
    );
  }

  @override
  State<NotificationSettingsDialog> createState() => _NotificationSettingsDialogState();
}

class _NotificationSettingsDialogState extends State<NotificationSettingsDialog> {
  bool _notificationsEnabled = true;
  String _reminderFrequency = 'Weekly';
  bool _quietHoursEnabled = false;
  TimeOfDay _quietStart = const TimeOfDay(hour: 22, minute: 0);
  TimeOfDay _quietEnd = const TimeOfDay(hour: 7, minute: 0);

  final List<String> _frequencies = ['Daily', 'Weekly', 'Bi-weekly'];

  Future<void> _selectTime(bool isStart) async {
    final picked = await showTimePicker(
      context: context,
      initialTime: isStart ? _quietStart : _quietEnd,
    );
    if (picked != null) {
      setState(() {
        if (isStart) {
          _quietStart = picked;
        } else {
          _quietEnd = picked;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return Padding(
      padding: EdgeInsets.only(
        left: 20,
        right: 20,
        top: 20,
        bottom: bottomInset + 20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Notification Preferences',
                style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
              ),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.pop(context),
              ),
            ],
          ),
          const Divider(),
          const SizedBox(height: 10),

          // Master Switch: Enable / Disable Notifications
          SwitchListTile(
            title: const Text('Enable Plant Monitoring Reminders'),
            subtitle: const Text('Receive scan reminders and worsening disease alerts.'),
            value: _notificationsEnabled,
            onChanged: (val) => setState(() => _notificationsEnabled = val),
          ),
          const SizedBox(height: 10),

          // Reminder Frequency Dropdown
          if (_notificationsEnabled) ...[
            ListTile(
              title: const Text('Reminder Frequency'),
              subtitle: const Text('How often to receive monitoring scan reminders'),
              trailing: DropdownButton<String>(
                value: _reminderFrequency,
                items: _frequencies.map((freq) {
                  return DropdownMenuItem(
                    value: freq,
                    child: Text(freq),
                  );
                }).toList(),
                onChanged: (val) {
                  if (val != null) setState(() => _reminderFrequency = val);
                },
              ),
            ),
            const Divider(),
            const SizedBox(height: 10),

            // Quiet Hours Toggle
            SwitchListTile(
              title: const Text('Configure Quiet Hours'),
              subtitle: const Text('Silence non-critical notifications during rest hours'),
              value: _quietHoursEnabled,
              onChanged: (val) => setState(() => _quietHoursEnabled = val),
            ),

            if (_quietHoursEnabled) ...[
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    TextButton.icon(
                      onPressed: () => _selectTime(true),
                      icon: const Icon(Icons.bedtime_outlined, size: 18),
                      label: Text('Start: ${_quietStart.format(context)}'),
                    ),
                    TextButton.icon(
                      onPressed: () => _selectTime(false),
                      icon: const Icon(Icons.wb_sunny_outlined, size: 18),
                      label: Text('End: ${_quietEnd.format(context)}'),
                    ),
                  ],
                ),
              ),
            ],
          ],

          const SizedBox(height: 20),

          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Notification settings updated successfully')),
                );
              },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              child: const Text('Save Preferences'),
            ),
          ),
        ],
      ),
    );
  }
}
