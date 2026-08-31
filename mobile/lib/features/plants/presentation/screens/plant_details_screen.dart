import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../models/plant_model.dart';
import '../../../../providers/auth_provider.dart';
import '../../../../providers/plant_provider.dart';
import '../../../../widgets/custom_card.dart';
import '../widgets/create_edit_plant_dialog.dart';
import '../widgets/plant_timeline_widget.dart';

class PlantDetailsScreen extends StatelessWidget {
  final PlantModel plant;

  const PlantDetailsScreen({super.key, required this.plant});

  void _confirmDelete(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete Plant Profile'),
        content: Text('Are you sure you want to delete "${plant.name}"? This action cannot be undone.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
            onPressed: () async {
              Navigator.of(ctx).pop();
              final authProvider = Provider.of<AuthProvider>(context, listen: false);
              final plantProvider = Provider.of<PlantProvider>(context, listen: false);
              final token = authProvider.token ?? 'guest_token';

              final success = await plantProvider.deletePlant(token: token, plantId: plant.id);
              if (success && context.mounted) {
                Navigator.of(context).pop();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Plant profile deleted')),
                );
              }
            },
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(plant.name),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit),
            onPressed: () => CreateEditPlantDialog.show(context, plant: plant),
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: Colors.red),
            onPressed: () => _confirmDelete(context),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Plant Card Header
            CustomCard(
              color: theme.colorScheme.primaryContainer,
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: const BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                    ),
                    child: Icon(Icons.eco, size: 36, color: theme.colorScheme.primary),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          plant.name,
                          style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        Text(
                          'Crop: ${plant.cropType}',
                          style: TextStyle(fontSize: 14, color: Colors.grey[700]),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Profile Details List
            CustomCard(
              child: Column(
                children: [
                  _DetailRow(
                    icon: Icons.grass,
                    title: 'Crop Type',
                    value: plant.cropType,
                  ),
                  const Divider(),
                  _DetailRow(
                    icon: Icons.nature,
                    title: 'Variety',
                    value: plant.variety ?? 'Standard Variety',
                  ),
                  const Divider(),
                  _DetailRow(
                    icon: Icons.location_on_outlined,
                    title: 'Location / Field',
                    value: plant.location ?? 'Not specified',
                  ),
                  const Divider(),
                  _DetailRow(
                    icon: Icons.calendar_month,
                    title: 'Planting Date',
                    value: plant.plantingDate != null
                        ? '${plant.plantingDate!.year}-${plant.plantingDate!.month.toString().padLeft(2, '0')}-${plant.plantingDate!.day.toString().padLeft(2, '0')}'
                        : 'Not specified',
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Notes Card
            if (plant.notes != null && plant.notes!.isNotEmpty) ...[
              CustomCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Notes & Observations',
                      style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      plant.notes!,
                      style: TextStyle(color: Colors.grey[800], height: 1.4),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
            ],

            // Plant Timeline & Health Progress Monitoring
            PlantTimelineWidget(plantId: plant.id),
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;

  const _DetailRow({
    required this.icon,
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: Theme.of(context).colorScheme.primary, size: 20),
          const SizedBox(width: 12),
          Text(title, style: TextStyle(color: Colors.grey[600], fontSize: 13)),
          const Spacer(),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        ],
      ),
    );
  }
}
