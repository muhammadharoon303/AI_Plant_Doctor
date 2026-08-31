import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../models/history_item_model.dart';
import '../../models/diagnosis_result.dart';
import '../../repositories/history_repository.dart';
import '../scanner/presentation/diagnosis_result_screen.dart';
import '../../widgets/custom_card.dart';

class HistoryScreen extends StatefulWidget {
  final String currentLanguage;

  const HistoryScreen({super.key, required this.currentLanguage});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final HistoryRepository _repository = HistoryRepository();
  final TextEditingController _searchController = TextEditingController();

  List<HistoryItemModel> _allHistory = [];
  List<HistoryItemModel> _filteredHistory = [];
  bool _isLoading = true;
  String? _errorMessage;
  String _selectedSeverityFilter = 'All';

  final List<String> _severityFilters = ['All', 'Severe', 'Moderate', 'Mild', 'Healthy'];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final items = await _repository.getDiagnosisHistory(
        searchQuery: _searchController.text.trim(),
      );
      setState(() {
        _allHistory = items;
        _applyFilters();
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  void _applyFilters() {
    final query = _searchController.text.toLowerCase().trim();

    setState(() {
      _filteredHistory = _allHistory.where((item) {
        final matchesQuery = query.isEmpty ||
            item.cropName.toLowerCase().contains(query) ||
            item.diseaseName.toLowerCase().contains(query) ||
            (item.plantName != null && item.plantName!.toLowerCase().contains(query));

        final matchesSeverity = _selectedSeverityFilter == 'All' ||
            item.severityStage.toLowerCase() == _selectedSeverityFilter.toLowerCase();

        return matchesQuery && matchesSeverity;
      }).toList();
    });
  }

  void _openDetailScreen(HistoryItemModel item) {
    final double conf = item.confidence <= 1.0 ? item.confidence : item.confidence / 100.0;
    final bool isHealthy = item.diseaseName.toLowerCase().contains('healthy');

    final result = DiagnosisResult(
      scanId: item.scanId,
      diseaseKey: item.diseaseKey,
      cropName: item.cropName,
      diseaseName: item.diseaseName,
      confidence: conf,
      modelVersion: item.modelVersion,
      affectedPercentage: item.affectedPercentage,
      severityStage: item.severityStage,
      isHealthy: isHealthy,
      imageUrl: item.imageUrl,
      maskUrl: item.maskUrl,
      description: 'Historical diagnosis scan record #${item.scanId}.',
      symptoms: 'Observed leaf lesions and surface discoloration consistent with ${item.diseaseName}.',
      biologicalTreatment: 'Apply organic neem oil and bio-fungicides if disease recurs.',
      chemicalTreatment: 'Use registered protective fungicides as per local extension guide.',
      prevention: 'Maintain healthy soil drainage, pruning, and crop rotation.',
      createdAt: item.createdAt,
    );

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => DiagnosisResultScreen(
          result: result,
          onRescan: () => Navigator.pop(context),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis Scan History'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadHistory,
            tooltip: 'Refresh History',
          ),
        ],
      ),
      body: Column(
        children: [
          // Search Bar & Filters Header
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                // Search Input Field
                TextField(
                  controller: _searchController,
                  onChanged: (_) => _applyFilters(),
                  decoration: InputDecoration(
                    hintText: 'Search by crop, disease, or plant name...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              _applyFilters();
                            },
                          )
                        : null,
                    filled: true,
                    fillColor: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                const SizedBox(height: 12),

                // Severity Filter Chips
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _severityFilters.map((filter) {
                      final isSelected = _selectedSeverityFilter == filter;
                      return Padding(
                        padding: const EdgeInsets.only(right: 8.0),
                        child: FilterChip(
                          label: Text(filter),
                          selected: isSelected,
                          onSelected: (selected) {
                            if (selected) {
                              setState(() {
                                _selectedSeverityFilter = filter;
                                _applyFilters();
                              });
                            }
                          },
                          selectedColor: theme.colorScheme.primaryContainer,
                          checkmarkColor: theme.colorScheme.primary,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ],
            ),
          ),

          // Main Content List / Loading / Error
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _errorMessage != null
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.error_outline, size: 48, color: Colors.red),
                            const SizedBox(height: 12),
                            Text(_errorMessage!, style: const TextStyle(color: Colors.red)),
                            const SizedBox(height: 12),
                            ElevatedButton(
                              onPressed: _loadHistory,
                              child: const Text('Retry'),
                            ),
                          ],
                        ),
                      )
                    : _filteredHistory.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.history_toggle_off, size: 64, color: Colors.grey.shade400),
                                const SizedBox(height: 12),
                                Text(
                                  _allHistory.isEmpty
                                      ? 'No diagnosis history records yet.'
                                      : 'No scans match your search filters.',
                                  style: TextStyle(color: Colors.grey.shade600, fontSize: 15),
                                ),
                              ],
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: _loadHistory,
                            child: ListView.builder(
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              itemCount: _filteredHistory.length,
                              itemBuilder: (context, index) {
                                final item = _filteredHistory[index];
                                final dateStr = DateFormat('MMM d, yyyy • h:mm a').format(item.createdAt);
                                final double confPct = item.confidence <= 1.0 ? item.confidence * 100.0 : item.confidence;
                                final bool isHealthy = item.diseaseName.toLowerCase().contains('healthy');

                                return Padding(
                                  padding: const EdgeInsets.only(bottom: 12.0),
                                  child: CustomCard(
                                    onTap: () => _openDetailScreen(item),
                                    child: Row(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        // Leaf Thumbnail Preview
                                        ClipRRect(
                                          borderRadius: BorderRadius.circular(12),
                                          child: Container(
                                            width: 72,
                                            height: 72,
                                            color: Colors.grey.shade200,
                                            child: item.imageUrl.isNotEmpty
                                                ? Image.network(
                                                    item.imageUrl,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (_, __, ___) => const Icon(Icons.eco, color: Colors.green),
                                                  )
                                                : const Icon(Icons.eco, color: Colors.green),
                                          ),
                                        ),
                                        const SizedBox(width: 14),

                                        // Diagnosis Record Details
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Row(
                                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                                children: [
                                                  Text(
                                                    '${item.cropName} • ${confPct.toStringAsFixed(1)}%',
                                                    style: TextStyle(
                                                      fontSize: 12,
                                                      fontWeight: FontWeight.bold,
                                                      color: theme.colorScheme.primary,
                                                    ),
                                                  ),
                                                  Chip(
                                                    label: Text(item.severityStage),
                                                    backgroundColor: isHealthy ? Colors.green.shade100 : Colors.orange.shade100,
                                                    visualDensity: VisualDensity.compact,
                                                    labelStyle: const TextStyle(fontSize: 10),
                                                  ),
                                                ],
                                              ),
                                              Text(
                                                item.diseaseName,
                                                style: const TextStyle(
                                                  fontSize: 16,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                              const SizedBox(height: 4),

                                              if (item.plantName != null && item.plantName!.isNotEmpty)
                                                Row(
                                                  children: [
                                                    const Icon(Icons.yard_outlined, size: 12, color: Colors.grey),
                                                    const SizedBox(width: 4),
                                                    Text(
                                                      'Plant: ${item.plantName}',
                                                      style: const TextStyle(fontSize: 11, color: Colors.grey),
                                                    ),
                                                  ],
                                                ),
                                              const SizedBox(height: 4),

                                              Text(
                                                dateStr,
                                                style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                );
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}
