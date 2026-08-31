class DiagnosisResult {
  final int scanId;
  final String diseaseKey;
  final String cropName;
  final String diseaseName;
  final String? scientificName;
  final double confidence;
  final String modelVersion;
  final double affectedPercentage;
  final String severityStage;
  final bool isHealthy;
  final String imageUrl;
  final String? maskUrl;
  final String description;
  final String symptoms;
  final String possibleCauses;
  final String management;
  final String biologicalTreatment;
  final String chemicalTreatment;
  final String prevention;
  final String safetyInformation;
  final List<String> sources;
  final DateTime createdAt;

  DiagnosisResult({
    required this.scanId,
    required this.diseaseKey,
    required this.cropName,
    required this.diseaseName,
    this.scientificName,
    required this.confidence,
    this.modelVersion = 'tomato-v1.0',
    required this.affectedPercentage,
    required this.severityStage,
    required this.isHealthy,
    required this.imageUrl,
    this.maskUrl,
    required this.description,
    required this.symptoms,
    this.possibleCauses = 'Fungal / Bacterial pathogen infection, high humidity',
    this.management = 'Prune infected foliage, improve field drainage and spacing',
    required this.biologicalTreatment,
    required this.chemicalTreatment,
    required this.prevention,
    this.safetyInformation = 'Observe 7-14 days Pre-Harvest Interval (PHI). Wear protective mask and gloves during chemical spray.',
    this.sources = const ['USDA Plant Pathology Extension', 'FAO Crop Protection Guide', 'CAB Direct Plantwise'],
    required this.createdAt,
  });

  factory DiagnosisResult.fromJson(Map<String, dynamic> json) {
    return DiagnosisResult(
      scanId: json['scan_id'] ?? 0,
      diseaseKey: json['disease_key'] ?? '',
      cropName: json['crop'] ?? (json['crop_name'] ?? 'Tomato'),
      diseaseName: json['disease'] ?? (json['disease_name'] ?? 'Healthy'),
      scientificName: json['scientific_name'],
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      modelVersion: json['model_version'] ?? 'tomato-v1.0',
      affectedPercentage: (json['affected_percentage'] as num?)?.toDouble() ?? 0.0,
      severityStage: json['severity_stage'] ?? 'Healthy',
      isHealthy: json['is_healthy'] ?? false,
      imageUrl: json['image_url'] ?? '',
      maskUrl: json['mask_url'],
      description: json['description'] ?? '',
      symptoms: json['symptoms'] ?? '',
      possibleCauses: json['possible_causes'] ?? 'Fungal / Bacterial pathogen infection, high humidity',
      management: json['management'] ?? (json['prevention'] ?? 'Prune infected foliage, improve field drainage and spacing'),
      biologicalTreatment: json['biological_treatment'] ?? '',
      chemicalTreatment: json['chemical_treatment'] ?? '',
      prevention: json['prevention'] ?? '',
      safetyInformation: json['safety_information'] ?? 'Observe 7-14 days Pre-Harvest Interval (PHI). Wear protective mask and gloves during chemical spray.',
      sources: json['sources'] != null ? List<String>.from(json['sources']) : const ['USDA Plant Pathology Extension', 'FAO Crop Protection Guide', 'CAB Direct Plantwise'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }
}
