import 'package:flutter_test/flutter_test.dart';
import 'package:ai_plant_doctor/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const PlantDoctorApp());
    expect(find.byType(PlantDoctorApp), findsOneWidget);
  });
}
