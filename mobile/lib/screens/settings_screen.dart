import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/generated/app_localizations.dart';
import '../providers/theme_provider.dart';
import '../providers/locale_provider.dart';
import '../providers/auth_provider.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_button.dart';
import '../core/constants/api_constants.dart';
import 'auth/login_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _serverUrlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _serverUrlController.text = ApiConstants.baseUrl;
  }

  @override
  void dispose() {
    _serverUrlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final localeProvider = Provider.of<LocaleProvider>(context);
    final authProvider = Provider.of<AuthProvider>(context);
    final l10n = AppLocalizations.of(context)!;
    final theme = Theme.of(context);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Account Profile Card
          CustomCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Account & Profile',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                const Divider(),
                if (authProvider.isAuthenticated) ...[
                  ListTile(
                    leading: CircleAvatar(
                      backgroundColor: theme.colorScheme.primary,
                      child: Text(
                        (authProvider.user?.fullName ?? authProvider.user?.email ?? 'F')[0].toUpperCase(),
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                    ),
                    title: Text(authProvider.user?.fullName ?? 'Farmer Account'),
                    subtitle: Text(authProvider.user?.email ?? ''),
                  ),
                  const SizedBox(height: 8),
                  CustomButton(
                    text: 'Log Out',
                    type: ButtonType.outline,
                    icon: Icons.logout,
                    onPressed: () async {
                      await authProvider.logout();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Logged out successfully')),
                        );
                      }
                    },
                  ),
                ] else ...[
                  const ListTile(
                    leading: Icon(Icons.account_circle, size: 40, color: Colors.grey),
                    title: Text('Guest Farmer'),
                    subtitle: Text('Sign in to sync plant profiles and scan history across devices'),
                  ),
                  const SizedBox(height: 8),
                  CustomButton(
                    text: 'Sign In / Register',
                    icon: Icons.login,
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => const LoginScreen()),
                      );
                    },
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Server Connection & Standalone Mode Card
          CustomCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.wifi_tethering, color: theme.colorScheme.primary),
                    const SizedBox(width: 8),
                    Text(
                      'Server Connection & Standalone AI',
                      style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const Divider(),
                const Text(
                  'When disconnected from USB laptop, the app uses Wi-Fi server connection or automatic On-Device Offline AI Diagnostics.',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _serverUrlController,
                  decoration: const InputDecoration(
                    labelText: 'Backend Server URL',
                    hintText: 'e.g. http://192.168.100.5:8000',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.dns),
                  ),
                ),
                const SizedBox(height: 10),
                CustomButton(
                  text: 'Save Server URL',
                  icon: Icons.save,
                  onPressed: () async {
                    await ApiConstants.setCustomServerUrl(_serverUrlController.text);
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Server URL updated successfully')),
                      );
                    }
                  },
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Appearance & Theme Card
          CustomCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Appearance & Theme',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                const Divider(),
                SwitchListTile(
                  title: const Text('Dark Mode'),
                  subtitle: const Text('Enable Material 3 dark theme'),
                  secondary: Icon(
                    themeProvider.isDarkMode ? Icons.dark_mode : Icons.light_mode,
                    color: theme.colorScheme.primary,
                  ),
                  value: themeProvider.isDarkMode,
                  onChanged: (bool value) {
                    themeProvider.toggleTheme(value);
                  },
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Language Selection Card
          CustomCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.languageSelect,
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.language, color: Colors.blue),
                  title: Text(l10n.english),
                  subtitle: const Text('English (LTR)'),
                  trailing: localeProvider.languageCode == 'en' ? const Icon(Icons.check_circle, color: Colors.green) : null,
                  onTap: () => localeProvider.setLanguageCode('en'),
                ),
                ListTile(
                  leading: const Icon(Icons.language, color: Colors.green),
                  title: Text(l10n.urdu),
                  subtitle: const Text('اردو (RTL)'),
                  trailing: localeProvider.languageCode == 'ur' ? const Icon(Icons.check_circle, color: Colors.green) : null,
                  onTap: () => localeProvider.setLanguageCode('ur'),
                ),
                ListTile(
                  leading: const Icon(Icons.language, color: Colors.orange),
                  title: Text(l10n.pashto),
                  subtitle: const Text('پښتو (RTL)'),
                  trailing: localeProvider.languageCode == 'ps' ? const Icon(Icons.check_circle, color: Colors.green) : null,
                  onTap: () => localeProvider.setLanguageCode('ps'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
