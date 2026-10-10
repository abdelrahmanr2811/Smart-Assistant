import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/theme/app_theme.dart';
import '../providers/chat_provider.dart';
import '../widgets/chat_bubble.dart';
import '../widgets/voice_recorder_button.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  final List<String> _quickSuggestions = [
    '📊 احسبلي مؤشرات الأداء الـ SPI والـ CPI',
    '📅 أنشطة الموقع لتاريخ اليوم',
    '🏗️ سجل توريدات الخرسانة وحديد التسليح',
    '👥 مين مسؤول الـ QA/QC ورقم تليفونه؟',
    '📧 ابعت إيميل لمهندس الموقع للمتابعة',
    '📝 تلخيص محضر اجتماع الموقع الأخير',
  ];

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _handleSend() {
    final text = _textController.text.trim();
    if (text.isEmpty) return;
    _textController.clear();
    ref.read(chatProvider.notifier).sendMessage(text);
    _scrollToBottom();
  }

  @override
  Widget build(BuildContext context) {
    final chatState = ref.watch(chatProvider);
    final chatNotifier = ref.read(chatProvider.notifier);

    // Auto-scroll on new message
    ref.listen(chatProvider, (previous, next) {
      if (previous?.messages.length != next.messages.length) {
        _scrollToBottom();
      }
    });

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: AppTheme.accent.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.architecture, color: AppTheme.accent, size: 20),
            ),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAlignment.start,
              children: const [
                Text('Smart Assistant', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                Text('Construction & Engineering PM AI', style: TextStyle(fontSize: 11, color: AppTheme.darkTextSecondary)),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_comment_outlined),
            tooltip: 'New Conversation',
            onPressed: () => chatNotifier.startNewSession(),
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Sessions',
            onPressed: () => chatNotifier.fetchSessions(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Quick suggestion chips
          Container(
            height: 44,
            margin: const EdgeInsets.symmetric(vertical: 6),
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: _quickSuggestions.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final suggestion = _quickSuggestions[index];
                return ActionChip(
                  backgroundColor: AppTheme.darkSurface,
                  side: const BorderSide(color: Color(0xFF334155)),
                  label: Text(
                    suggestion,
                    style: const TextStyle(fontSize: 12, color: AppTheme.darkTextPrimary),
                  ),
                  onPressed: () {
                    ref.read(chatProvider.notifier).sendMessage(suggestion);
                    _scrollToBottom();
                  },
                );
              },
            ),
          ),

          const Divider(height: 1, color: Color(0xFF334155)),

          // Messages List
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(vertical: 12),
              itemCount: chatState.messages.length,
              itemBuilder: (context, index) {
                final msg = chatState.messages[index];
                return ChatBubble(
                  message: msg,
                  onApproveAction: (actionId, updatedParams) {
                    chatNotifier.approveAction(actionId, updatedParams);
                  },
                  onRejectAction: (actionId) {
                    chatNotifier.rejectAction(actionId);
                  },
                );
              },
            ),
          ),

          // Loading Indicator
          if (chatState.isLoading) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              child: Row(
                children: const [
                  SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.accent),
                  ),
                  SizedBox(width: 10),
                  Text(
                    'Smart Assistant is analyzing project data...',
                    style: TextStyle(fontSize: 12, color: AppTheme.darkTextSecondary),
                  ),
                ],
              ),
            ),
          ],

          // Bottom Input Bar
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.darkSurface,
              border: const Border(top: BorderSide(color: Color(0xFF334155), width: 1)),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  // Voice Push-to-Talk FAB
                  const VoiceRecorderButton(),
                  const SizedBox(width: 10),

                  // Text Input
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      minLines: 1,
                      maxLines: 4,
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _handleSend(),
                      decoration: InputDecoration(
                        hintText: 'Ask about schedule, materials, EVM, staff, or speak in Arabic/English...',
                        suffixIcon: IconButton(
                          icon: const Icon(Icons.send_rounded, color: AppTheme.primary),
                          onPressed: _handleSend,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
