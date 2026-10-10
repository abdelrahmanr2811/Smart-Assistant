import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/api_constants.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late Dio dio;
  String _baseUrl = ApiConstants.defaultBaseUrl;

  ApiClient._internal() {
    dio = Dio(
      BaseOptions(
        baseUrl: _baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 45),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    dio.interceptors.add(
      LogInterceptor(
        request: true,
        requestHeader: false,
        requestBody: true,
        responseBody: true,
        error: true,
      ),
    );
  }

  Future<void> init() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedUrl = prefs.getString('custom_backend_url');
      if (savedUrl != null && savedUrl.isNotEmpty) {
        updateBaseUrl(savedUrl);
      }
    } catch (e) {
      debugPrint('Error loading saved base URL: $e');
    }
  }

  void updateBaseUrl(String newUrl) {
    _baseUrl = newUrl.endsWith('/') ? newUrl.substring(0, newUrl.length - 1) : newUrl;
    dio.options.baseUrl = _baseUrl;
  }

  String get baseUrl => _baseUrl;

  // 1. Send Chat Message
  Future<Response> sendChatMessage({
    required String message,
    String? sessionId,
    String? provider,
  }) async {
    return await dio.post(
      ApiConstants.chatMessage,
      data: {
        'message': message,
        if (sessionId != null) 'session_id': sessionId,
        if (provider != null) 'provider': provider,
      },
    );
  }

  // 2. Fetch Sessions
  Future<Response> getSessions() async {
    return await dio.get(ApiConstants.chatSessions);
  }

  // 3. Fetch Session Messages
  Future<Response> getSessionMessages(String sessionId) async {
    return await dio.get('${ApiConstants.sessionMessages}/$sessionId/messages');
  }

  // 4. Action Approvals (HITL)
  Future<Response> approveAction({
    required String actionId,
    Map<String, dynamic>? parameters,
  }) async {
    return await dio.post(
      ApiConstants.actionApprove,
      data: {
        'action_id': actionId,
        if (parameters != null) 'parameters': parameters,
      },
    );
  }

  Future<Response> rejectAction(String actionId) async {
    return await dio.post(
      ApiConstants.actionReject,
      data: {'action_id': actionId},
    );
  }

  // 5. Upload Document
  Future<Response> uploadDocument({
    required String filePath,
    required String fileName,
    required String category,
    Uint8List? fileBytes,
  }) async {
    MultipartFile multipartFile;
    if (kIsWeb && fileBytes != null) {
      multipartFile = MultipartFile.fromBytes(fileBytes, filename: fileName);
    } else {
      multipartFile = await MultipartFile.fromFile(filePath, filename: fileName);
    }

    final formData = FormData.fromMap({
      'file': multipartFile,
      'category': category,
    });

    return await dio.post(ApiConstants.documentsUpload, data: formData);
  }

  // 6. Fetch Documents & KPI Summary
  Future<Response> getDocumentsList() async {
    return await dio.get(ApiConstants.documentsList);
  }

  Future<Response> getKpiSummary() async {
    return await dio.get(ApiConstants.documentsKpi);
  }

  // 7. Voice Pipeline (Transcribe & Run directly through agent)
  Future<Response> sendVoiceCommand({
    required String audioPath,
    Uint8List? audioBytes,
    String? sessionId,
  }) async {
    MultipartFile audioFile;
    if (kIsWeb && audioBytes != null) {
      audioFile = MultipartFile.fromBytes(audioBytes, filename: 'voice_command.wav');
    } else {
      audioFile = await MultipartFile.fromFile(audioPath, filename: 'voice_command.wav');
    }

    final formData = FormData.fromMap({
      'file': audioFile,
      if (sessionId != null) 'session_id': sessionId,
    });

    return await dio.post(ApiConstants.voiceTranscribeAndRun, data: formData);
  }
}
