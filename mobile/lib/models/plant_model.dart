class PlantModel {
  final int id;
  final int userId;
  final String name;
  final String cropType;
  final String? variety;
  final DateTime? plantingDate;
  final String? location;
  final String? notes;
  final DateTime createdAt;

  PlantModel({
    required this.id,
    required this.userId,
    required this.name,
    required this.cropType,
    this.variety,
    this.plantingDate,
    this.location,
    this.notes,
    required this.createdAt,
  });

  factory PlantModel.fromJson(Map<String, dynamic> json) {
    return PlantModel(
      id: json['id'] ?? 0,
      userId: json['user_id'] ?? 0,
      name: json['name'] ?? '',
      cropType: json['crop_type'] ?? '',
      variety: json['variety'],
      plantingDate: json['planting_date'] != null ? DateTime.parse(json['planting_date']) : null,
      location: json['location'],
      notes: json['notes'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'name': name,
      'crop_type': cropType,
      'variety': variety,
      'planting_date': plantingDate?.toIso8601String(),
      'location': location,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
