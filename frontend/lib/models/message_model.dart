import 'action_card_model.dart';

class MessageModel {
  final String id;
  final String sessionId;
  final String role; // 'user', 'assistant', 'system'
  final String content;
  final DateTime createdAt;
  final ActionCardModel? actionRequired;
  final bool isAudio;

  MessageModel({
    required this.id,
    required this.sessionId,
    required this.role,
    required this.content,
    required this.createdAt,
    this.actionRequired,
    this.isAudio = false,
  });

  factory MessageModel.fromJson(Map<String, dynamic> json) {
    ActionCardModel? action;
    if (json['action_required'] != null) {
      action = ActionCardModel.fromJson(Map<String, dynamic>.from(json['action_required']));
    }

    return MessageModel(
      id: json['id']?.toString() ?? DateTime.now().millisecondsSinceEpoch.toString(),
      sessionId: json['session_id'] ?? '',
      role: json['role'] ?? 'user',
      content: json['content'] ?? '',
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at']) ?? DateTime.now()
          : DateTime.now(),
      actionRequired: action,
      isAudio: json['is_audio'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'session_id': sessionId,
      'role': role,
      'content': content,
      'created_at': createdAt.toIso8601String(),
      'action_required': actionRequired?.toJson(),
      'is_audio': isAudio,
    };
  }
}
