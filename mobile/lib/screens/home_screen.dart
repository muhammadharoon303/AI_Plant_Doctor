import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/generated/app_localizations.dart';

import '../providers/locale_provider.dart';
import '../providers/theme_provider.dart';
import '../widgets/responsive_layout.dart';
import '../features/scanner/presentation/scanner_screen.dart';
import '../features/history/history_screen.dart';
import '../features/knowledge_base/knowledge_screen.dart';
import '../features/assistant/assistant_screen.dart';
import 'dashboard_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  void _navigateToTab(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  Widget _buildAttractiveBottomNavBar(BuildContext context, AppLocalizations l10n) {
    final navItems = [
      {'icon': Icons.space_dashboard_outlined, 'activeIcon': Icons.space_dashboard_rounded, 'label': 'Dashboard'},
      {'icon': Icons.qr_code_scanner_outlined, 'activeIcon': Icons.qr_code_scanner_rounded, 'label': l10n.scannerTab},
      {'icon': Icons.history_outlined, 'activeIcon': Icons.history_rounded, 'label': l10n.historyTab},
      {'icon': Icons.menu_book_outlined, 'activeIcon': Icons.menu_book_rounded, 'label': l10n.knowledgeTab},
      {'icon': Icons.support_agent_outlined, 'activeIcon': Icons.support_agent_rounded, 'label': l10n.assistantTab},
      {'icon': Icons.settings_outlined, 'activeIcon': Icons.settings_rounded, 'label': 'Settings'},
    ];

    return SafeArea(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF1B4332), Color(0xFF2D6A4F)],
            begin: Alignment.centerLeft,
            end: Alignment.centerRight,
          ),
          borderRadius: BorderRadius.circular(32),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF1B4332).withValues(alpha: 0.40),
              blurRadius: 18,
              offset: const Offset(0, 8),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: List.generate(navItems.length, (index) {
            final item = navItems[index];
            final isSelected = _selectedIndex == index;

            return Tooltip(
              message: item['label'] as String,
              child: GestureDetector(
                onTap: () => _navigateToTab(index),
                behavior: HitTestBehavior.opaque,
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 250),
                  curve: Curves.easeInOut,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: isSelected ? Colors.white.withValues(alpha: 0.24) : Colors.transparent,
                    borderRadius: BorderRadius.circular(24),
                    border: isSelected ? Border.all(color: Colors.white38, width: 1) : null,
                  ),
                  child: Icon(
                    isSelected ? (item['activeIcon'] as IconData) : (item['icon'] as IconData),
                    color: isSelected ? Colors.white : Colors.white60,
                    size: isSelected ? 26 : 22,
                  ),
                ),
              ),
            );
          }),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final localeProvider = Provider.of<LocaleProvider>(context);
    final themeProvider = Provider.of<ThemeProvider>(context);

    final List<Widget> screens = [
      DashboardScreen(
        onQuickScan: () => _navigateToTab(1),
        onOpenLibrary: () => _navigateToTab(3),
        onOpenAssistant: () => _navigateToTab(4),
      ),
      ScannerScreen(currentLanguage: localeProvider.languageCode),
      HistoryScreen(currentLanguage: localeProvider.languageCode),
      KnowledgeScreen(currentLanguage: localeProvider.languageCode),
      AssistantScreen(currentLanguage: localeProvider.languageCode),
      const SettingsScreen(),
    ];

    return Directionality(
      textDirection: localeProvider.isRtl ? TextDirection.rtl : TextDirection.ltr,
      child: Scaffold(
        appBar: AppBar(
          title: Text(l10n.appTitle),
          actions: [
            IconButton(
              icon: Icon(themeProvider.isDarkMode ? Icons.light_mode : Icons.dark_mode),
              onPressed: () {
                themeProvider.toggleTheme(!themeProvider.isDarkMode);
              },
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.language),
              onSelected: (String langCode) {
                localeProvider.setLanguageCode(langCode);
              },
              itemBuilder: (BuildContext context) => [
                PopupMenuItem(value: 'en', child: Text(l10n.english)),
                PopupMenuItem(value: 'ur', child: Text(l10n.urdu)),
                PopupMenuItem(value: 'ps', child: Text(l10n.pashto)),
              ],
            ),
          ],
        ),
        body: ResponsiveLayout(
          mobile: IndexedStack(
            index: _selectedIndex,
            children: screens,
          ),
          desktop: Row(
            children: [
              NavigationRail(
                selectedIndex: _selectedIndex,
                onDestinationSelected: _navigateToTab,
                labelType: NavigationRailLabelType.all,
                destinations: [
                  const NavigationRailDestination(
                    icon: Icon(Icons.space_dashboard_rounded),
                    label: Text('Dashboard'),
                  ),
                  NavigationRailDestination(
                    icon: const Icon(Icons.qr_code_scanner),
                    label: Text(l10n.scannerTab),
                  ),
                  NavigationRailDestination(
                    icon: const Icon(Icons.history),
                    label: Text(l10n.historyTab),
                  ),
                  NavigationRailDestination(
                    icon: const Icon(Icons.menu_book),
                    label: Text(l10n.knowledgeTab),
                  ),
                  NavigationRailDestination(
                    icon: const Icon(Icons.support_agent),
                    label: Text(l10n.assistantTab),
                  ),
                  const NavigationRailDestination(
                    icon: Icon(Icons.settings),
                    label: Text('Settings'),
                  ),
                ],
              ),
              const VerticalDivider(thickness: 1, width: 1),
              Expanded(
                child: IndexedStack(
                  index: _selectedIndex,
                  children: screens,
                ),
              ),
            ],
          ),
        ),
        bottomNavigationBar: ResponsiveLayout.isDesktop(context)
            ? null
            : _buildAttractiveBottomNavBar(context, l10n),
      ),
    );
  }
}
