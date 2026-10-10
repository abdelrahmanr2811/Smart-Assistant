import 'package:flutter/foundation.dart';

class ApiConstants {
  // Default Base URLs
  static const String defaultLocalhost = 'http://127.0.0.1:8000';
  static const String defaultAndroidEmulator = 'http://10.0.2.2:8000';

  static String get defaultBaseUrl {
    if (kIsWeb) {
      return defaultLocalhost;
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      return defaultAndroidEmulator;
    } else {
      return defaultLocalhost;
    }
  }

  // Endpoints
  static const String chatMessage = '/api/v1/chat/message';
  static const String chatSessions = '/api/v1/chat/sessions';
  static const String sessionMessages = '/api/v1/chat/sessions';
  
  static const String actionsPending = '/api/v1/actions/pending';
  static const String actionApprove = '/api/v1/actions/approve';
  static const String actionReject = '/api/v1/actions/reject';

  static const String documentsUpload = '/api/v1/documents/upload';
  static const String documentsList = '/api/v1/documents/list';
  static const String documentsKpi = '/api/v1/documents/kpi-summary';

  static const String voiceTranscribe = '/api/v1/voice/transcribe';
  static const String voiceTranscribeAndRun = '/api/v1/voice/transcribe-and-run';
}
