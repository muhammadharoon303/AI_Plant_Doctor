import 'package:flutter/material.dart';

class SegmentationOverlayWidget extends StatefulWidget {
  final String imageUrl;
  final String? maskUrl;

  const SegmentationOverlayWidget({
    super.key,
    required this.imageUrl,
    this.maskUrl,
  });

  @override
  State<SegmentationOverlayWidget> createState() => _SegmentationOverlayWidgetState();
}

class _SegmentationOverlayWidgetState extends State<SegmentationOverlayWidget> {
  bool _showMask = true;

  @override
  Widget build(BuildContext context) {
    final String activeUrl = (_showMask && widget.maskUrl != null) ? widget.maskUrl! : widget.imageUrl;

    return Column(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: AspectRatio(
            aspectRatio: 1.0,
            child: Image.network(
              activeUrl,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) => Container(
                color: Colors.grey[200],
                child: const Icon(Icons.broken_image, size: 64, color: Colors.grey),
              ),
            ),
          ),
        ),
        const SizedBox(height: 12),
        if (widget.maskUrl != null)
          SegmentedButton<bool>(
            segments: const [
              ButtonSegment<bool>(
                value: true,
                label: Text("AI Lesion Mask"),
                icon: Icon(Icons.blur_on),
              ),
              ButtonSegment<bool>(
                value: false,
                label: Text("Original Leaf"),
                icon: Icon(Icons.image),
              ),
            ],
            selected: {_showMask},
            onSelectionChanged: (Set<bool> newSelection) {
              setState(() {
                _showMask = newSelection.first;
              });
            },
          ),
      ],
    );
  }
}
