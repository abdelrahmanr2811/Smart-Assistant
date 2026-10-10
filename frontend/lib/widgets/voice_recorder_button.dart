import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/theme/app_theme.dart';
import '../providers/voice_provider.dart';

class VoiceRecorderButton extends ConsumerStatefulWidget {
  const VoiceRecorderButton({super.key});

  @override
  ConsumerState<VoiceRecorderButton> createState() => _VoiceRecorderButtonState();
}

class _VoiceRecorderButtonState extends ConsumerState<VoiceRecorderButton> with SingleTickerProviderStateMixin {
  late AnimationController _animController;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  String _formatDuration(int seconds) {
    final mins = (seconds ~/ 60).toString().padLeft(2, '0');
    final secs = (seconds % 60).toString().padLeft(2, '0');
    return '$mins:$secs';
  }

  @override
  Widget build(BuildContext context) {
    final voiceState = ref.watch(voiceProvider);
    final voiceNotifier = ref.read(voiceProvider.notifier);

    if (voiceState.isProcessing) {
      return Container(
        height: 52,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        decoration: BoxDecoration(
          color: AppTheme.darkSurface,
          borderRadius: BorderRadius.circular(26),
          border: Border.all(color: AppTheme.primary, width: 1.5),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2.5, color: AppTheme.primary),
            ),
            SizedBox(width: 10),
            Text(
              'Transcribing Voice (Whisper)...',
              style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppTheme.darkTextPrimary),
            ),
          ],
        ),
      );
    }

    if (voiceState.isRecording) {
      return AnimatedBuilder(
        animation: _animController,
        builder: (context, child) {
          return InkWell(
            onTap: () => voiceNotifier.stopAndProcessRecording(),
            borderRadius: BorderRadius.circular(26),
            child: Container(
              height: 52,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: AppTheme.danger.withOpacity(0.15 + (_animController.value * 0.15)),
                borderRadius: BorderRadius.circular(26),
                border: Border.all(color: AppTheme.danger, width: 2),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.danger.withOpacity(0.3 * _animController.value),
                    blurRadius: 12,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 12,
                    height: 12,
                    decoration: const BoxDecoration(
                      color: AppTheme.danger,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Recording ${_formatDuration(voiceState.durationSeconds)}',
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.danger,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Icon(Icons.stop_circle, color: AppTheme.danger, size: 22),
                  const SizedBox(width: 4),
                  const Text(
                    '(Tap to Send)',
                    style: TextStyle(fontSize: 11, color: AppTheme.darkTextSecondary),
                  ),
                ],
              ),
            ),
          );
        },
      );
    }

    // Default Idle Microphone Button
    return Tooltip(
      message: 'Push-to-Talk Voice Command (Egyptian Arabic & English)',
      child: Material(
        color: AppTheme.accent,
        borderRadius: BorderRadius.circular(26),
        elevation: 3,
        child: InkWell(
          onTap: () => voiceNotifier.startRecording(),
          borderRadius: BorderRadius.circular(26),
          child: Container(
            height: 48,
            width: 48,
            alignment: Alignment.center,
            child: const Icon(Icons.mic, color: Colors.black87, size: 24),
          ),
        ),
      ),
    );
  }
}
