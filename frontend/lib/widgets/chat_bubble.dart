import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:intl/intl.dart';
import '../core/theme/app_theme.dart';
import '../models/message_model.dart';
import 'action_approval_card.dart';

class ChatBubble extends StatelessWidget {
  final MessageModel message;
  final Function(String actionId, Map<String, dynamic>? updatedParams)? onApproveAction;
  final Function(String actionId)? onRejectAction;

  const ChatBubble({
    super.key,
    required this.message,
    this.onApproveAction,
    this.onRejectAction,
  });

  bool get isUser => message.role == 'user';

  @override
  Widget build(BuildContext context) {
    final timeStr = DateFormat('hh:mm a').format(message.createdAt);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Column(
        crossAxisAlignment: isUser ? CrossAlignment.end : CrossAlignment.start,
        children: [
          // Role header & avatar
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (!isUser) ...[
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: AppTheme.primary.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.engineering, size: 16, color: AppTheme.primary),
                ),
                const SizedBox(width: 8),
                const Text(
                  'Smart Assistant',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.accent),
                ),
                const SizedBox(width: 8),
              ],
              Text(
                timeStr,
                style: const TextStyle(fontSize: 11, color: AppTheme.darkTextSecondary),
              ),
              if (isUser) ...[
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: AppTheme.accent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.person, size: 16, color: AppTheme.accent),
                ),
              ],
            ],
          ),
          const SizedBox(height: 6),

          // Message bubble container
          Container(
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * (MediaQuery.of(context).size.width > 800 ? 0.7 : 0.88),
            ),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: isUser ? AppTheme.primary : AppTheme.darkSurface,
              borderRadius: BorderRadius.only(
                topLeft: const Radius.circular(16),
                topRight: const Radius.circular(16),
                bottomLeft: isUser ? const Radius.circular(16) : const Radius.circular(4),
                bottomRight: isUser ? const Radius.circular(4) : const Radius.circular(16),
              ),
              border: Border.all(
                color: isUser ? AppTheme.primaryDark : const Color(0xFF334155),
                width: 1,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.15),
                  blurRadius: 6,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAlignment.start,
              children: [
                // Markdown or text
                MarkdownBody(
                  data: message.content,
                  selectable: true,
                  styleSheet: MarkdownStyleSheet(
                    p: TextStyle(
                      color: isUser ? Colors.white : AppTheme.darkTextPrimary,
                      fontSize: 14.5,
                      height: 1.5,
                    ),
                    h1: const TextStyle(color: AppTheme.accent, fontWeight: FontWeight.bold, fontSize: 18),
                    h2: const TextStyle(color: AppTheme.accent, fontWeight: FontWeight.bold, fontSize: 16),
                    h3: const TextStyle(color: AppTheme.accent, fontWeight: FontWeight.bold, fontSize: 15),
                    code: TextStyle(
                      backgroundColor: Colors.black.withOpacity(0.3),
                      color: AppTheme.accent,
                      fontSize: 13,
                      fontFamily: 'monospace',
                    ),
                    codeblockDecoration: BoxDecoration(
                      color: const Color(0xFF0F172A),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    tableBorder: TableBorder.all(color: const Color(0xFF475569), width: 1),
                    tableHead: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.accent),
                    tableBody: const TextStyle(color: AppTheme.darkTextPrimary, fontSize: 13),
                    tableHeadAlign: TextAlign.center,
                  ),
                ),

                // Copy button for assistant responses
                if (!isUser) ...[
                  const SizedBox(height: 10),
                  Align(
                    alignment: Alignment.bottomRight,
                    child: InkWell(
                      onTap: () {
                        Clipboard.setData(ClipboardData(text: message.content));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Content copied to clipboard!'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      },
                      borderRadius: BorderRadius.circular(6),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: const [
                            Icon(Icons.copy, size: 13, color: AppTheme.darkTextSecondary),
                            SizedBox(width: 4),
                            Text('Copy', style: TextStyle(fontSize: 11, color: AppTheme.darkTextSecondary)),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),

          // Interactive Action Card (if present)
          if (message.actionRequired != null) ...[
            const SizedBox(height: 8),
            ActionApprovalCard(
              action: message.actionRequired!,
              onApprove: (params) => onApproveAction?.call(message.actionRequired!.actionId, params),
              onReject: () => onRejectAction?.call(message.actionRequired!.actionId),
            ),
          ],
        ],
      ),
    );
  }
}
