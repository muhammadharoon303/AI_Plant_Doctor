import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../models/plant_model.dart';
import '../../../../providers/auth_provider.dart';
import '../../../../providers/plant_provider.dart';
import '../../../../widgets/custom_input.dart';
import '../../../../widgets/custom_button.dart';

class CreateEditPlantDialog extends StatefulWidget {
  final PlantModel? plant;

  const CreateEditPlantDialog({super.key, this.plant});

  static void show(BuildContext context, {PlantModel? plant}) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (_) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom,
        ),
        child: CreateEditPlantDialog(plant: plant),
      ),
    );
  }

  @override
  State<CreateEditPlantDialog> createState() => _CreateEditPlantDialogState();
}

class _CreateEditPlantDialogState extends State<CreateEditPlantDialog> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _cropController;
  late TextEditingController _varietyController;
  late TextEditingController _locationController;
  late TextEditingController _notesController;
  DateTime? _selectedDate;

  final List<String> _popularCrops = [
    'Tomato',
    'Potato',
    'Corn',
    'Wheat',
    'Apple',
    'Cotton',
    'Rice',
    'Other'
  ];

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.plant?.name ?? '');
    _cropController = TextEditingController(text: widget.plant?.cropType ?? 'Tomato');
    _varietyController = TextEditingController(text: widget.plant?.variety ?? '');
    _locationController = TextEditingController(text: widget.plant?.location ?? '');
    _notesController = TextEditingController(text: widget.plant?.notes ?? '');
    _selectedDate = widget.plant?.plantingDate;
  }

  void _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate ?? DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() => _selectedDate = picked);
    }
  }

  void _save() async {
    final name = _nameController.text.trim();
    final crop = _cropController.text.trim();

    if (name.isEmpty || crop.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in required fields (Name & Crop)')),
      );
      return;
    }

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final plantProvider = Provider.of<PlantProvider>(context, listen: false);
    final token = authProvider.token ?? 'guest_token';

    bool success = false;
    if (widget.plant == null) {
      success = await plantProvider.createPlant(
        token: token,
        name: name,
        cropType: crop,
        variety: _varietyController.text.trim().isEmpty ? null : _varietyController.text.trim(),
        plantingDate: _selectedDate,
        location: _locationController.text.trim().isEmpty ? null : _locationController.text.trim(),
        notes: _notesController.text.trim().isEmpty ? null : _notesController.text.trim(),
      );
    } else {
      success = await plantProvider.updatePlant(
        token: token,
        plantId: widget.plant!.id,
        name: name,
        cropType: crop,
        variety: _varietyController.text.trim().isEmpty ? null : _varietyController.text.trim(),
        plantingDate: _selectedDate,
        location: _locationController.text.trim().isEmpty ? null : _locationController.text.trim(),
        notes: _notesController.text.trim().isEmpty ? null : _notesController.text.trim(),
      );
    }

    if (success && mounted) {
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(widget.plant == null ? 'Plant Profile Created!' : 'Plant Profile Updated!'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final plantProvider = Provider.of<PlantProvider>(context);
    final isEditing = widget.plant != null;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              isEditing ? 'Edit Plant Profile' : 'Add New Plant Profile',
              style: theme.textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
                color: theme.colorScheme.primary,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),

            CustomInput(
              label: 'Plant Name *',
              hint: 'e.g., North Greenhouse Row 1',
              controller: _nameController,
              prefixIcon: Icons.eco,
            ),
            const SizedBox(height: 14),

            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Crop Type *', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                const SizedBox(height: 6),
                DropdownButtonFormField<String>(
                  initialValue: _popularCrops.contains(_cropController.text) ? _cropController.text : 'Tomato',
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.grass),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                  items: _popularCrops.map((crop) {
                    return DropdownMenuItem(value: crop, child: Text(crop));
                  }).toList(),
                  onChanged: (val) {
                    if (val != null) _cropController.text = val;
                  },
                ),
              ],
            ),
            const SizedBox(height: 14),

            CustomInput(
              label: 'Variety (Optional)',
              hint: 'e.g., Cherry Tomato / Roma',
              controller: _varietyController,
              prefixIcon: Icons.nature,
            ),
            const SizedBox(height: 14),

            CustomInput(
              label: 'Location / Field (Optional)',
              hint: 'e.g., Field B / Greenhouse 2',
              controller: _locationController,
              prefixIcon: Icons.location_on_outlined,
            ),
            const SizedBox(height: 14),

            // Planting Date Picker Row
            Row(
              children: [
                Expanded(
                  child: Text(
                    _selectedDate == null
                        ? 'Planting Date: Not set'
                        : 'Planting Date: ${_selectedDate!.year}-${_selectedDate!.month.toString().padLeft(2, '0')}-${_selectedDate!.day.toString().padLeft(2, '0')}',
                    style: TextStyle(color: Colors.grey[700], fontSize: 14),
                  ),
                ),
                OutlinedButton.icon(
                  onPressed: _pickDate,
                  icon: const Icon(Icons.calendar_month, size: 18),
                  label: const Text('Pick Date'),
                ),
              ],
            ),
            const SizedBox(height: 14),

            CustomInput(
              label: 'Notes (Optional)',
              hint: 'e.g., Fertilizer schedule, soil notes...',
              controller: _notesController,
              prefixIcon: Icons.notes,
              maxLines: 3,
            ),
            const SizedBox(height: 24),

            CustomButton(
              text: isEditing ? 'Save Changes' : 'Create Plant Profile',
              isLoading: plantProvider.isLoading,
              onPressed: _save,
            ),
          ],
        ),
      ),
    );
  }
}
