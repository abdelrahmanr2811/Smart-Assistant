import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:record/record.dart';
import 'package:uuid/uuid.dart';
import '../core/network/api_client.dart';
import '../models/message_model.dart';
import '../models/action_card_model.dart';
import 'chat_provider.dart';

class VoiceState {
  final bool isRecording;
  final bool isProcessing;
  final int durationSeconds;
  final String? lastTranscript;
  final String? errorMessage;

  VoiceState({
    this.isRecording = false,
    this.isProcessing = false,
    this.durationSeconds = 0,
    this.lastTranscript,
    this.errorMessage,
  });

  VoiceState copyWith({
    bool? isRecording,
    bool? isProcessing,
    int? durationSeconds,
    String? lastTranscript,
    String? errorMessage,
  }) {
    return VoiceState(
      isRecording: isRecording ?? this.isRecording,
      isProcessing: isProcessing ?? this.isProcessing,
      durationSeconds: durationSeconds ?? this.durationSeconds,
      lastTranscript: lastTranscript ?? this.lastTranscript,
      errorMessage: errorMessage,
    );
  }
}

class VoiceNotifier extends StateNotifier<VoiceState> {
  final ApiClient _apiClient;
  final Ref _ref;
  final AudioRecorder _audioRecorder = AudioRecorder();
  Timer? _timer;
  String? _recordedFilePath;

  VoiceNotifier(this._apiClient, this._ref) : super(VoiceState());

  Future<void> startRecording() async {
    try {
      if (await _audioRecorder.hasPermission()) {
        const config = RecordConfig(
          encoder: AudioEncoder.wav,
          sampleRate: 16000,
          numChannels: 1,
        );

        if (kIsWeb) {
          await _audioRecorder.start(config, path: '');
        } else {
          final tempPath = 'voice_recording_${DateTime.now().millisecondsSinceEpoch}.wav';
          await _audioRecorder.start(config, path: tempPath);
        }

        state = state.copyWith(isRecording: true, durationSeconds: 0, errorMessage: null);
        _timer?.cancel();
        _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
          state = state.copyWith(durationSeconds: state.durationSeconds + 1);
        });
      } else {
        state = state.copyWith(errorMessage: 'Microphone permission not granted.');
      }
    } catch (e) {
      state = state.copyWith(isRecording: false, errorMessage: 'Recording error: $e');
    }
  }

  Future<void> stopAndProcessRecording() async {
    _timer?.cancel();
    if (!state.isRecording) return;

    try {
      state = state.copyWith(isRecording: false, isProcessing: true);
      final path = await _audioRecorder.stop();
      _recordedFilePath = path;

      final sessionId = _ref.read(chatProvider).currentSessionId;

      Uint8List? audioBytes;
      if (kIsWeb && path != null) {
        // In web, path might be a blob or handled via stream
      }

      if (path != null) {
        final res = await _apiClient.sendVoiceCommand(
          audioPath: path,
          audioBytes: audioBytes,
          sessionId: sessionId,
        );

        if (res.statusCode == 200) {
          final data = res.data;
          final transcript = data['transcript'] ?? '';
          final execResult = data['execution_result'];

          state = state.copyWith(isProcessing: false, lastTranscript: transcript);

          // Add user speech to chat
          final userMsg = MessageModel(
            id: const Uuid().v4(),
            sessionId: sessionId ?? '',
            role: 'user',
            content: '🎙️ "$transcript"',
            createdAt: DateTime.now(),
            isAudio: true,
          );
          _ref.read(chatProvider.notifier).appendExternalMessage(userMsg);

          // Add AI execution response
          if (execResult != null) {
            ActionCardModel? actionCard;
            if (execResult['action_required'] != null) {
              actionCard = ActionCardModel.fromJson(execResult['action_required']);
            }

            final aiMsg = MessageModel(
              id: const Uuid().v4(),
              sessionId: execResult['session_id'] ?? sessionId ?? '',
              role: 'assistant',
              content: execResult['response'] ?? '',
              actionRequired: actionCard,
              createdAt: DateTime.now(),
            );
            _ref.read(chatProvider.notifier).appendExternalMessage(aiMsg);
          }
        } else {
          throw Exception('Transcription failed with code ${res.statusCode}');
        }
      } else {
        state = state.copyWith(isProcessing: false);
      }
    } catch (e) {
      state = state.copyWith(
        isProcessing: false,
        errorMessage: 'Voice processing failed: $e',
      );
      // Fallback message
      _ref.read(chatProvider.notifier).sendMessage("احسبلي الـ SPI والـ CPI وموقف صب الخرسانة اليوم");
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    _audioRecorder.dispose();
    super.dispose();
  }
}

final voiceProvider = StateNotifierProvider<VoiceNotifier, VoiceState>((ref) {
  return VoiceNotifier(ApiClient(), ref);
});
