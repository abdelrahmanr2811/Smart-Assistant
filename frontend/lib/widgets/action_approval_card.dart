import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../models/action_card_model.dart';

class ActionApprovalCard extends StatefulWidget {
  final ActionCardModel action;
  final Function(Map<String, dynamic>? updatedParams) onApprove;
  final VoidCallback onReject;

  const ActionApprovalCard({
    super.key,
    required this.action,
    required this.onApprove,
    required this.onReject,
  });

  @override
  State<ActionApprovalCard> createState() => _ActionApprovalCardState();
}

class _ActionApprovalCardState extends State<ActionApprovalCard> {
  bool _isEditing = false;
  late TextEditingController _toController;
  late TextEditingController _subjectController;
  late TextEditingController _bodyController;

  @override
  void initState() {
    super.initState();
    final p = widget.action.parameters;
    _toController = TextEditingController(text: p['to'] ?? p['attendees']?.toString() ?? '');
    _subjectController = TextEditingController(text: p['subject'] ?? p['title'] ?? '');
    _bodyController = TextEditingController(text: p['body'] ?? p['message'] ?? '');
  }

  @override
  void dispose() {
    _toController.dispose();
    _subjectController.dispose();
    _bodyController.dispose();
    super.dispose();
  }

  Color get _statusColor {
    switch (widget.action.status) {
      case 'EXECUTED':
        return AppTheme.success;
      case 'REJECTED':
        return AppTheme.danger;
      case 'FAILED':
        return AppTheme.danger;
      default:
        return AppTheme.accent;
    }
  }

  IconData get _toolIcon {
    if (widget.action.tool.contains('email')) {
      return Icons.email_outlined;
    } else if (widget.action.tool.contains('meeting') || widget.action.tool.contains('calendar')) {
      return Icons.calendar_month_outlined;
    }
    return Icons.build_circle_outlined;
  }

  void _showEditDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppTheme.darkSurface,
        title: Text('Edit Action Parameters (${widget.action.tool})'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _toController,
                decoration: const InputDecoration(labelText: 'Recipient / Attendees'),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _subjectController,
                decoration: const InputDecoration(labelText: 'Subject / Title'),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _bodyController,
                maxLines: 4,
                decoration: const InputDecoration(labelText: 'Body / Message'),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(ctx);
              final updated = Map<String, dynamic>.from(widget.action.parameters);
              if (updated.containsKey('to')) updated['to'] = _toController.text;
              if (updated.containsKey('subject')) updated['subject'] = _subjectController.text;
              if (updated.containsKey('body')) updated['body'] = _bodyController.text;
              if (updated.containsKey('title')) updated['title'] = _subjectController.text;
              
              widget.onApprove(updated);
            },
            child: const Text('Save & Approve'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isPending = widget.action.status == 'PENDING_CONFIRMATION';

    return Container(
      constraints: const BoxConstraints(maxWidth: 580),
      margin: const EdgeInsets.only(top: 4),
      decoration: BoxDecoration(
        color: AppTheme.darkCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: _statusColor.withOpacity(0.8),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: _statusColor.withOpacity(0.12),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAlignment.start,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.25),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(15),
                topRight: Radius.circular(15),
              ),
            ),
            child: Row(
              children: [
                Icon(_toolIcon, color: _statusColor, size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    widget.action.previewTitle ?? 'Human-In-The-Loop Action Required',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                      color: AppTheme.darkTextPrimary,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: _statusColor.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: _statusColor, width: 0.8),
                  ),
                  child: Text(
                    widget.action.status.replaceAll('_', ' '),
                    style: TextStyle(
                      color: _statusColor,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Parameters details body
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAlignment.start,
              children: [
                if (widget.action.previewDetails != null) ...[
                  ...widget.action.previewDetails!.entries.map((e) => Padding(
                        padding: const EdgeInsets.only(bottom: 6.0),
                        child: Row(
                          crossAxisAlignment: CrossAlignment.start,
                          children: [
                            SizedBox(
                              width: 90,
                              child: Text(
                                '${e.key}:',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12.5,
                                  color: AppTheme.darkTextSecondary,
                                ),
                              ),
                            ),
                            Expanded(
                              child: Text(
                                '${e.value}',
                                style: const TextStyle(fontSize: 13, color: AppTheme.darkTextPrimary),
                              ),
                            ),
                          ],
                        ),
                      )),
                ] else ...[
                  Text(
                    'Parameters: ${widget.action.parameters}',
                    style: const TextStyle(fontSize: 12, color: AppTheme.darkTextSecondary),
                  ),
                ],

                if (widget.action.executionMessage != null) ...[
                  const Divider(color: Color(0xFF475569), height: 16),
                  Row(
                    children: [
                      Icon(
                        widget.action.status == 'EXECUTED' ? Icons.check_circle : Icons.info,
                        color: _statusColor,
                        size: 16,
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          widget.action.executionMessage!,
                          style: TextStyle(fontSize: 12, color: _statusColor, fontWeight: FontWeight.w600),
                        ),
                      ),
                    ],
                  ),
                ],

                // Action Buttons
                if (isPending) ...[
                  const SizedBox(height: 14),
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => widget.onApprove(null),
                          icon: const Icon(Icons.check, size: 16),
                          label: const Text('Approve & Send'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.success,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 10),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      OutlinedButton.icon(
                        onPressed: _showEditDialog,
                        icon: const Icon(Icons.edit, size: 16),
                        label: const Text('Edit'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppTheme.accent,
                          side: const BorderSide(color: AppTheme.accent),
                          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                        ),
                      ),
                      const SizedBox(width: 8),
                      OutlinedButton(
                        onPressed: widget.onReject,
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppTheme.danger,
                          side: const BorderSide(color: AppTheme.danger),
                          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                        ),
                        child: const Text('Reject'),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
