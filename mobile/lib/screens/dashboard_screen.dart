import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/plant_provider.dart';
import '../widgets/dashboard/greeting_header_widget.dart';
import '../widgets/dashboard/health_summary_card_widget.dart';
import '../widgets/dashboard/quick_actions_grid_widget.dart';
import '../widgets/dashboard/disease_alerts_widget.dart';
import '../widgets/dashboard/my_plants_list_widget.dart';
import '../widgets/dashboard/recent_scans_list_widget.dart';
import '../widgets/dashboard/monitoring_reminders_widget.dart';
import '../features/plants/presentation/widgets/create_edit_plant_dialog.dart';

class DashboardScreen extends StatelessWidget {
  final VoidCallback onQuickScan;
  final VoidCallback onOpenAssistant;
  final VoidCallback onOpenLibrary;

  const DashboardScreen({
    super.key,
    required this.onQuickScan,
    required this.onOpenAssistant,
    required this.onOpenLibrary,
  });

  @override
  Widget build(BuildContext context) {
    final plantProvider = Provider.of<PlantProvider>(context);

    return RefreshIndicator(
      onRefresh: () async {
        await plantProvider.loadDiseases();
      },
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Greeting & User Profile Header
            const GreetingHeaderWidget(),
            const SizedBox(height: 16),

            // 2. Plant Health Metrics Summary
            const HealthSummaryCardWidget(
              totalScans: 0,
              healthyPercentage: 100.0,
              activeAlertsCount: 1,
            ),
            const SizedBox(height: 16),

            // 3. Quick Actions (Quick Scan, AI Assistant, Disease Library)
            QuickActionsGridWidget(
              onQuickScan: onQuickScan,
              onOpenAssistant: onOpenAssistant,
              onOpenLibrary: onOpenLibrary,
            ),
            const SizedBox(height: 16),

            // 4. Regional Disease Risk Alert
            const DiseaseAlertsWidget(),
            const SizedBox(height: 16),

            // 5. My Tracked Plants (with realistic empty state)
            MyPlantsListWidget(
              plants: plantProvider.userPlants,
              onAddPlant: () => CreateEditPlantDialog.show(context),
            ),
            const SizedBox(height: 16),

            // 6. Recent Diagnoses (with realistic empty state)
            RecentScansListWidget(
              recentScans: const [],
              onStartScan: onQuickScan,
            ),
            const SizedBox(height: 16),

            // 7. Monitoring Reminders
            const MonitoringRemindersWidget(),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
