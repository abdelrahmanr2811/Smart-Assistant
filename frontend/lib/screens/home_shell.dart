import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/theme/app_theme.dart';
import '../providers/chat_provider.dart';
import 'chat_screen.dart';
import 'project_kpi_screen.dart';
import 'document_upload_screen.dart';
import 'settings_screen.dart';

class HomeShell extends ConsumerStatefulWidget {
  const HomeShell({super.key});

  @override
  ConsumerState<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends ConsumerState<HomeShell> {
  int _selectedIndex = 0;

  final List<Widget> _screens = const [
    ChatScreen(),
    ProjectKpiScreen(),
    DocumentUploadScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final isDesktopOrWeb = MediaQuery.of(context).size.width > 750;
    final chatState = ref.watch(chatProvider);

    if (isDesktopOrWeb) {
      // Desktop / Web Dual-Pane Sidebar Layout
      return Scaffold(
        body: Row(
          children: [
            // Left Navigation Sidebar
            Container(
              width: 250,
              decoration: const BoxDecoration(
                color: AppTheme.darkSurface,
                border: Border(right: BorderSide(color: Color(0xFF334155), width: 1)),
              ),
              child: Column(
                children: [
                  // App Branding
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
                    alignment: Alignment.centerLeft,
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: AppTheme.primary,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: const Icon(Icons.architecture, color: Colors.white, size: 24),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAlignment.start,
                          children: const [
                            Text(
                              'Smart Assistant',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            Text(
                              'Construction PM AI',
                              style: TextStyle(fontSize: 11, color: AppTheme.accent),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const Divider(color: Color(0xFF334155), height: 1),

                  // Navigation Items
                  Expanded(
                    child: ListView(
                      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 10),
                      children: [
                        _buildNavTile(
                          index: 0,
                          icon: Icons.chat_bubble_outline,
                          selectedIcon: Icons.chat_bubble,
                          title: 'PM Assistant Chat',
                        ),
                        _buildNavTile(
                          index: 1,
                          icon: Icons.analytics_outlined,
                          selectedIcon: Icons.analytics,
                          title: 'EVM KPI Dashboard',
                        ),
                        _buildNavTile(
                          index: 2,
                          icon: Icons.folder_shared_outlined,
                          selectedIcon: Icons.folder_shared,
                          title: 'Knowledge Base (RAG)',
                        ),
                        _buildNavTile(
                          index: 3,
                          icon: Icons.settings_outlined,
                          selectedIcon: Icons.settings,
                          title: 'Settings & Config',
                        ),

                        if (_selectedIndex == 0 && chatState.sessions.isNotEmpty) ...[
                          const Padding(
                            padding: EdgeInsets.only(top: 20, left: 12, bottom: 8),
                            child: Text(
                              'RECENT SESSIONS',
                              style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.darkTextSecondary),
                            ),
                          ),
                          ...chatState.sessions.take(5).map((s) {
                            final isCurrent = s['session_id'] == chatState.currentSessionId;
                            return ListTile(
                              dense: true,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                              selected: isCurrent,
                              selectedTileColor: AppTheme.primary.withOpacity(0.15),
                              leading: Icon(Icons.chat, size: 14, color: isCurrent ? AppTheme.accent : AppTheme.darkTextSecondary),
                              title: Text(
                                s['title'] ?? 'Session',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: isCurrent ? AppTheme.accent : AppTheme.darkTextPrimary,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                              onTap: () => ref.read(chatProvider.notifier).switchSession(s['session_id']),
                            );
                          }),
                        ],
                      ],
                    ),
                  ),

                  // User / Status Footer
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: const BoxDecoration(
                      border: Border(top: BorderSide(color: Color(0xFF334155), width: 1)),
                    ),
                    child: Row(
                      children: [
                        Container(
                          width: 10,
                          height: 10,
                          decoration: const BoxDecoration(
                            color: AppTheme.success,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        const Text(
                          'Backend: Connected',
                          style: TextStyle(fontSize: 11.5, color: AppTheme.darkTextSecondary),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            // Right Main Content
            Expanded(
              child: _screens[_selectedIndex],
            ),
          ],
        ),
      );
    }

    // Mobile Layout with Bottom Navigation Bar
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (idx) => setState(() => _selectedIndex = idx),
        backgroundColor: AppTheme.darkSurface,
        indicatorColor: AppTheme.primary.withOpacity(0.3),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.chat_bubble_outline),
            selectedIcon: Icon(Icons.chat_bubble, color: AppTheme.accent),
            label: 'Chat',
          ),
          NavigationDestination(
            icon: Icon(Icons.analytics_outlined),
            selectedIcon: Icon(Icons.analytics, color: AppTheme.accent),
            label: 'EVM KPIs',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder_shared_outlined),
            selectedIcon: Icon(Icons.folder_shared, color: AppTheme.accent),
            label: 'Documents',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings, color: AppTheme.accent),
            label: 'Settings',
          ),
        ],
      ),
    );
  }

  Widget _buildNavTile({
    required int index,
    required IconData icon,
    required IconData selectedIcon,
    required String title,
  }) {
    final isSelected = _selectedIndex == index;
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      decoration: BoxDecoration(
        color: isSelected ? AppTheme.primary : Colors.transparent,
        borderRadius: BorderRadius.circular(10),
      ),
      child: ListTile(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        leading: Icon(
          isSelected ? selectedIcon : icon,
          color: isSelected ? Colors.white : AppTheme.darkTextSecondary,
          size: 20,
        ),
        title: Text(
          title,
          style: TextStyle(
            color: isSelected ? Colors.white : AppTheme.darkTextPrimary,
            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            fontSize: 13.5,
          ),
        ),
        onTap: () => setState(() => _selectedIndex = index),
      ),
    );
  }
}
