class ActionCardModel {
  final String actionId;
  final String tool;
  final Map<String, dynamic> parameters;
  final String? previewTitle;
  final Map<String, dynamic>? previewDetails;
  String status; // 'PENDING_CONFIRMATION', 'EXECUTED', 'REJECTED', 'FAILED'
  String? executionMessage;

  ActionCardModel({
    required this.actionId,
    required this.tool,
    required this.parameters,
    this.previewTitle,
    this.previewDetails,
    this.status = 'PENDING_CONFIRMATION',
    this.executionMessage,
  });

  factory ActionCardModel.fromJson(Map<String, dynamic> json) {
    return ActionCardModel(
      actionId: json['action_id'] ?? '',
      tool: json['tool'] ?? '',
      parameters: Map<String, dynamic>.from(json['parameters'] ?? {}),
      previewTitle: json['preview_title'],
      previewDetails: json['preview_details'] != null
          ? Map<String, dynamic>.from(json['preview_details'])
          : null,
      status: json['status'] ?? 'PENDING_CONFIRMATION',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': 'ACTION_REQUIRED',
      'action_id': actionId,
      'tool': tool,
      'parameters': parameters,
      'preview_title': previewTitle,
      'preview_details': previewDetails,
      'status': status,
    };
  }
}
