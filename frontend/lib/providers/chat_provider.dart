import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';
import '../core/network/api_client.dart';
import '../models/message_model.dart';
import '../models/action_card_model.dart';

class ChatState {
  final List<MessageModel> messages;
  final List<Map<String, dynamic>> sessions;
  final String? currentSessionId;
  final bool isLoading;
  final String? errorMessage;

  ChatState({
    this.messages = const [],
    this.sessions = const [],
    this.currentSessionId,
    this.isLoading = false,
    this.errorMessage,
  });

  ChatState copyWith({
    List<MessageModel>? messages,
    List<Map<String, dynamic>>? sessions,
    String? currentSessionId,
    bool? isLoading,
    String? errorMessage,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      sessions: sessions ?? this.sessions,
      currentSessionId: currentSessionId ?? this.currentSessionId,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
    );
  }
}

class ChatNotifier extends StateNotifier<ChatState> {
  final ApiClient _apiClient;
  final _uuid = const Uuid();

  ChatNotifier(this._apiClient) : super(ChatState()) {
    _initInitialSession();
  }

  void _initInitialSession() {
    final newSessionId = 'sess_${_uuid.v4().substring(0, 8)}';
    state = state.copyWith(
      currentSessionId: newSessionId,
      messages: [
        MessageModel(
          id: 'welcome_1',
          sessionId: newSessionId,
          role: 'assistant',
          content: '👷‍♂️ **مرحباً بك يا باشمهندس! أنا مساعدك الذكي Smart Assistant لإدارة المشروعات الهندسية والإنشائية.**\n\n'
              'يمكنك التحدث معي باللغة العربية أو الإنجليزية أو بالصوت عبر الميكروفون بالأسفل:\n'
              '• 📊 متابعة مؤشرات الأداء (EVM / SPI / CPI) والجداول الزمنية\n'
              '• 🏗️ متابعة أنشطة الموقع وصب الخرسانة والتوريدات\n'
              '• 👥 دليل فريق العمل والتواصل مع المهندسين\n'
              '• ⚡ اتخاذ الإجراءات التفاعلية (إرسال إيميلات / جدولة اجتماعات)',
          createdAt: DateTime.now(),
        ),
      ],
    );
    fetchSessions();
  }

  Future<void> fetchSessions() async {
    try {
      final res = await _apiClient.getSessions();
      if (res.statusCode == 200 && res.data is List) {
        state = state.copyWith(sessions: List<Map<String, dynamic>>.from(res.data));
      }
    } catch (e) {
      // Offline fallback
    }
  }

  void startNewSession() {
    final newSessionId = 'sess_${_uuid.v4().substring(0, 8)}';
    state = state.copyWith(
      currentSessionId: newSessionId,
      messages: [
        MessageModel(
          id: 'welcome_${DateTime.now().millisecondsSinceEpoch}',
          sessionId: newSessionId,
          role: 'assistant',
          content: 'محادثة جديدة نشطة. تفضل بسؤالك أو أرسل أمرك الصوتي.',
          createdAt: DateTime.now(),
        ),
      ],
    );
  }

  Future<void> switchSession(String sessionId) async {
    state = state.copyWith(isLoading: true, currentSessionId: sessionId);
    try {
      final res = await _apiClient.getSessionMessages(sessionId);
      if (res.statusCode == 200 && res.data is List) {
        final msgs = (res.data as List).map((m) => MessageModel.fromJson(m)).toList();
        state = state.copyWith(messages: msgs, isLoading: false);
      }
    } catch (e) {
      state = state.copyWith(isLoading: false, errorMessage: 'Failed to load session: $e');
    }
  }

  Future<void> sendMessage(String text, {String? provider}) async {
    if (text.trim().isEmpty) return;

    final userMsg = MessageModel(
      id: _uuid.v4(),
      sessionId: state.currentSessionId ?? 'sess_default',
      role: 'user',
      content: text,
      createdAt: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMsg],
      isLoading: true,
      errorMessage: null,
    );

    try {
      final response = await _apiClient.sendChatMessage(
        message: text,
        sessionId: state.currentSessionId,
        provider: provider,
      );

      if (response.statusCode == 200) {
        final data = response.data;
        ActionCardModel? actionCard;
        if (data['action_required'] != null) {
          actionCard = ActionCardModel.fromJson(data['action_required']);
        }

        final aiMsg = MessageModel(
          id: _uuid.v4(),
          sessionId: data['session_id'] ?? state.currentSessionId ?? '',
          role: 'assistant',
          content: data['response'] ?? '',
          actionRequired: actionCard,
          createdAt: DateTime.now(),
        );

        state = state.copyWith(
          messages: [...state.messages, aiMsg],
          currentSessionId: data['session_id'] ?? state.currentSessionId,
          isLoading: false,
        );
        fetchSessions();
      } else {
        throw Exception('Server returned status ${response.statusCode}');
      }
    } catch (e) {
      final errorMsg = MessageModel(
        id: _uuid.v4(),
        sessionId: state.currentSessionId ?? '',
        role: 'assistant',
        content: '⚠️ حدث خطأ في الاتصال بالخادم. يرجى التأكد من تشغيل السيرفر.\n\n*التفاصيل:* `$e`',
        createdAt: DateTime.now(),
      );
      state = state.copyWith(
        messages: [...state.messages, errorMsg],
        isLoading: false,
      );
    }
  }

  void appendExternalMessage(MessageModel msg) {
    state = state.copyWith(messages: [...state.messages, msg]);
  }

  Future<void> approveAction(String actionId, Map<String, dynamic>? updatedParams) async {
    try {
      final res = await _apiClient.approveAction(actionId: actionId, parameters: updatedParams);
      if (res.statusCode == 200) {
        final resData = res.data;
        _updateActionStatusInMessages(actionId, 'EXECUTED', resData['message']);
      }
    } catch (e) {
      _updateActionStatusInMessages(actionId, 'FAILED', 'Failed to execute: $e');
    }
  }

  Future<void> rejectAction(String actionId) async {
    try {
      final res = await _apiClient.rejectAction(actionId);
      if (res.statusCode == 200) {
        _updateActionStatusInMessages(actionId, 'REJECTED', 'Cancelled by user');
      }
    } catch (e) {
      _updateActionStatusInMessages(actionId, 'REJECTED', 'Cancelled');
    }
  }

  void _updateActionStatusInMessages(String actionId, String newStatus, String? message) {
    final updated = state.messages.map((m) {
      if (m.actionRequired != null && m.actionRequired!.actionId == actionId) {
        final updatedAction = ActionCardModel(
          actionId: m.actionRequired!.actionId,
          tool: m.actionRequired!.tool,
          parameters: m.actionRequired!.parameters,
          previewTitle: m.actionRequired!.previewTitle,
          previewDetails: m.actionRequired!.previewDetails,
          status: newStatus,
          executionMessage: message,
        );
        return MessageModel(
          id: m.id,
          sessionId: m.sessionId,
          role: m.role,
          content: m.content,
          actionRequired: updatedAction,
          createdAt: m.createdAt,
          isAudio: m.isAudio,
        );
      }
      return m;
    }).toList();

    state = state.copyWith(messages: updated);
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  return ChatNotifier(ApiClient());
});
