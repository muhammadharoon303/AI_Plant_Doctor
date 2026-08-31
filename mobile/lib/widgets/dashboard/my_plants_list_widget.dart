import 'package:flutter/material.dart';
import '../../models/plant_model.dart';
import '../../features/plants/presentation/screens/plant_details_screen.dart';

class MyPlantsListWidget extends StatelessWidget {
  final List<PlantModel> plants;
  final VoidCallback onAddPlant;

  const MyPlantsListWidget({
    super.key,
    required this.plants,
    required this.onAddPlant,
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
              'My Tracked Plants',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            IconButton(
              icon: const Icon(Icons.add_circle, color: Colors.green),
              onPressed: onAddPlant,
              tooltip: 'Add Plant Profile',
            ),
          ],
        ),
        const SizedBox(height: 8),

        if (plants.isEmpty)
          // Realistic Empty State
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.grey.shade300),
            ),
            child: Column(
              children: [
                Icon(Icons.nature_people_rounded, size: 48, color: Colors.grey[400]),
                const SizedBox(height: 10),
                Text(
                  'No plants added yet',
                  style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700]),
                ),
                const SizedBox(height: 4),
                Text(
                  'Track individual crops in your farm or greenhouse to monitor health over time.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: onAddPlant,
                  icon: const Icon(Icons.add, size: 18),
                  label: const Text('Add My First Plant'),
                ),
              ],
            ),
          )
        else
          SizedBox(
            height: 120,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: plants.length,
              itemBuilder: (context, index) {
                final plant = plants[index];
                return InkWell(
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => PlantDetailsScreen(plant: plant)),
                    );
                  },
                  borderRadius: BorderRadius.circular(16),
                  child: Container(
                    width: 140,
                    margin: const EdgeInsets.only(right: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 8,
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.eco, color: Colors.green, size: 20),
                            const SizedBox(width: 6),
                            Expanded(
                              child: Text(
                                plant.cropType,
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: Colors.grey,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          plant.name,
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const Spacer(),
                        Text(
                          plant.variety ?? (plant.location ?? 'Standard'),
                          style: TextStyle(fontSize: 11, color: Colors.grey[600]),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
      ],
    );
  }
}
