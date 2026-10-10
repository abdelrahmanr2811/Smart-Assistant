import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/constants/api_constants.dart';
import '../core/network/api_client.dart';
import '../core/theme/app_theme.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late TextEditingController _urlController;
  String _selectedProvider = 'openai';
  String _selectedWhisper = 'openai_cloud';
  bool _requireApproval = true;
  bool _isTesting = false;
  String? _testResult;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController(text: ApiClient().baseUrl);
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _selectedProvider = prefs.getString('llm_provider') ?? 'openai';
      _selectedWhisper = prefs.getString('whisper_mode') ?? 'openai_cloud';
      _requireApproval = prefs.getBool('hitl_required') ?? true;
    });
  }

  Future<void> _saveSettings() async {
    final prefs = await SharedPreferences.getInstance();
    final newUrl = _urlController.text.trim();
    if (newUrl.isNotEmpty) {
      await prefs.setString('custom_backend_url', newUrl);
      ApiClient().updateBaseUrl(newUrl);
    }
    await prefs.setString('llm_provider', _selectedProvider);
    await prefs.setString('whisper_mode', _selectedWhisper);
    await prefs.setBool('hitl_required', _requireApproval);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Settings saved successfully!'),
          backgroundColor: AppTheme.success,
        ),
      );
    }
  }

  Future<void> _testConnection() async {
    setState(() {
      _isTesting = true;
      _testResult = null;
    });

    try {
      final res = await ApiClient().dio.get('${_urlController.text.trim()}/health');
      if (res.statusCode == 200) {
        setState(() {
          _isTesting = false;
          _testResult = '✅ Connected successfully to Smart Assistant Backend!';
        });
      } else {
        setState(() {
          _isTesting = false;
          _testResult = '⚠️ Server responded with code ${res.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _isTesting = false;
        _testResult = '❌ Connection failed: $e';
      });
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('System Configuration & Settings'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAlignment.start,
          children: [
            // Backend URL Card
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: AppTheme.darkSurface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                crossAxisAlignment: CrossAlignment.start,
                children: [
                  const Text(
                    'Backend Server Connection',
                    style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Set the FastAPI server host. (Windows localhost: http://127.0.0.1:8000, Android emulator: http://10.0.2.2:8000, or local LAN IP).',
                    style: TextStyle(fontSize: 12.5, color: AppTheme.darkTextSecondary),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _urlController,
                    decoration: const InputDecoration(
                      labelText: 'Server Base URL',
                      prefixIcon: Icon(Icons.dns, color: AppTheme.accent),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      ElevatedButton.icon(
                        onPressed: _saveSettings,
                        icon: const Icon(Icons.save, size: 16),
                        label: const Text('Save URL'),
                      ),
                      const SizedBox(width: 10),
                      OutlinedButton.icon(
                        onPressed: _isTesting ? null : _testConnection,
                        icon: _isTesting
                            ? const SizedBox(
                                width: 14,
                                height: 14,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : const Icon(Icons.bolt, size: 16),
                        label: const Text('Test Connection'),
                        style: OutlinedButton.styleFrom(foregroundColor: AppTheme.accent),
                      ),
                    ],
                  ),
                  if (_testResult != null) ...[
                    const SizedBox(height: 10),
                    Text(_testResult!, style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.bold)),
                  ],
                ],
              ),
            ),

            const SizedBox(height: 20),

            // LLM Model Provider
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: AppTheme.darkSurface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                crossAxisAlignment: CrossAlignment.start,
                children: [
                  const Text(
                    'AI Intelligence Engine',
                    style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                  ),
                  const SizedBox(height: 12),
                  RadioListTile<String>(
                    title: const Text('OpenAI GPT-4o (High Performance)'),
                    subtitle: const Text('Full construction reasoning & multi-turn tool calling'),
                    value: 'openai',
                    groupValue: _selectedProvider,
                    onChanged: (v) => setState(() => _selectedProvider = v!),
                  ),
                  RadioListTile<String>(
                    title: const Text('Google Gemini 1.5 Pro / Flash'),
                    subtitle: const Text('Extended multimodal context & technical office reasoning'),
                    value: 'gemini',
                    groupValue: _selectedProvider,
                    onChanged: (v) => setState(() => _selectedProvider = v!),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // HITL Safety Protocol
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: AppTheme.darkSurface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: SwitchListTile(
                title: const Text(
                  'Human-In-The-Loop Safety Protocol',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14.5),
                ),
                subtitle: const Text(
                  'Require explicit PM manual confirmation before dispatching emails or scheduling calendar meetings.',
                  style: TextStyle(fontSize: 12, color: AppTheme.darkTextSecondary),
                ),
                value: _requireApproval,
                activeColor: AppTheme.accent,
                onChanged: (v) => setState(() => _requireApproval = v),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
