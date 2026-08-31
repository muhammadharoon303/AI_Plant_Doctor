class HistoryItemModel {
  final int id;
  final int scanId;
  final String diseaseKey;
  final String cropName;
  final String diseaseName;
  final double confidence;
  final String modelVersion;
  final bool segmentationStatus;
  final double affectedPercentage;
  final String severityStage;
  final String imageUrl;
  final String? maskUrl;
  final int? plantId;
  final String? plantName;
  final DateTime createdAt;

  HistoryItemModel({
    required this.id,
    required this.scanId,
    required this.diseaseKey,
    required this.cropName,
    required this.diseaseName,
    required this.confidence,
    this.modelVersion = 'tomato-v1.0',
    this.segmentationStatus = true,
    required this.affectedPercentage,
    required this.severityStage,
    required this.imageUrl,
    this.maskUrl,
    this.plantId,
    this.plantName,
    required this.createdAt,
  });

  factory HistoryItemModel.fromJson(Map<String, dynamic> json) {
    return HistoryItemModel(
      id: json['id'] ?? json['scan_id'] ?? 0,
      scanId: json['scan_id'] ?? json['id'] ?? 0,
      diseaseKey: json['disease_key'] ?? '',
      cropName: json['crop'] ?? (json['crop_name'] ?? 'Tomato'),
      diseaseName: json['disease'] ?? (json['disease_name'] ?? 'Healthy'),
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      modelVersion: json['model_version'] ?? 'tomato-v1.0',
      segmentationStatus: json['segmentation_status'] ?? true,
      affectedPercentage: (json['affected_percentage'] as num?)?.toDouble() ?? 0.0,
      severityStage: json['severity_stage'] ?? 'Healthy',
      imageUrl: json['image_url'] ?? '',
      maskUrl: json['mask_url'],
      plantId: json['plant_id'],
      plantName: json['plant_name'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }
}
