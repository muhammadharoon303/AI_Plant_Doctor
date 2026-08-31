class LocalizedDiseaseInfo {
  final String name;
  final String description;
  final String symptoms;
  final String biologicalTreatment;
  final String chemicalTreatment;
  final String prevention;

  LocalizedDiseaseInfo({
    required this.name,
    required this.description,
    required this.symptoms,
    required this.biologicalTreatment,
    required this.chemicalTreatment,
    required this.prevention,
  });

  factory LocalizedDiseaseInfo.fromJson(Map<String, dynamic> json) {
    return LocalizedDiseaseInfo(
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      symptoms: json['symptoms'] ?? '',
      biologicalTreatment: json['biological_treatment'] ?? '',
      chemicalTreatment: json['chemical_treatment'] ?? '',
      prevention: json['prevention'] ?? '',
    );
  }
}

class DiseaseModel {
  final int id;
  final String diseaseKey;
  final String cropName;
  final String? scientificName;
  final String category;
  final LocalizedDiseaseInfo localizedInfo;
  final DateTime createdAt;

  DiseaseModel({
    required this.id,
    required this.diseaseKey,
    required this.cropName,
    this.scientificName,
    required this.category,
    required this.localizedInfo,
    required this.createdAt,
  });

  factory DiseaseModel.fromJson(Map<String, dynamic> json) {
    return DiseaseModel(
      id: json['id'] ?? 0,
      diseaseKey: json['disease_key'] ?? '',
      cropName: json['crop_name'] ?? '',
      scientificName: json['scientific_name'],
      category: json['category'] ?? 'Fungal',
      localizedInfo: LocalizedDiseaseInfo.fromJson(json['localized_info'] ?? {}),
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }
}
