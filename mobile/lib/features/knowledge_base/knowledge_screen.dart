import 'package:flutter/material.dart';

class KnowledgeScreen extends StatelessWidget {
  final String currentLanguage;
  const KnowledgeScreen({super.key, required this.currentLanguage});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: ListTile(
            leading: const Icon(Icons.local_florist, color: Colors.red),
            title: const Text("Tomato Early Blight"),
            subtitle: const Text("Alternaria solani • Fungal"),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {},
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.grass, color: Colors.purple),
            title: const Text("Potato Late Blight"),
            subtitle: const Text("Phytophthora infestans • Oomycete"),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {},
          ),
        ),
      ],
    );
  }
}
