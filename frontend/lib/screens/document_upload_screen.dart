import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import 'package:intl/intl.dart';
import '../core/theme/app_theme.dart';
import '../providers/doc_provider.dart';

class DocumentUploadScreen extends ConsumerStatefulWidget {
  const DocumentUploadScreen({super.key});

  @override
  ConsumerState<DocumentUploadScreen> createState() => _DocumentUploadScreenState();
}

class _DocumentUploadScreenState extends ConsumerState<DocumentUploadScreen> {
  String _selectedCategory = 'Schedule';
  final List<String> _categories = [
    'Schedule',
    'Materials & BOQ',
    'Staff Directory',
    'Meeting Transcripts',
    'General',
  ];

  Future<void> _pickAndUploadFile() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'xlsx', 'xls', 'csv', 'txt', 'docx'],
        withData: kIsWeb,
      );

      if (result != null && result.files.isNotEmpty) {
        final file = result.files.first;
        final success = await ref.read(docProvider.notifier).uploadFile(
              filePath: file.path ?? '',
              fileName: file.name,
              category: _selectedCategory,
              fileBytes: file.bytes,
            );

        if (success && mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('File "${file.name}" indexed successfully into ChromaDB!'),
              backgroundColor: AppTheme.success,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error selecting file: $e'),
            backgroundColor: AppTheme.danger,
          ),
        );
      }
    }
  }

  IconData _getCategoryIcon(String category) {
    if (category.contains('Schedule')) return Icons.calendar_month;
    if (category.contains('Materials') || category.contains('BOQ')) return Icons.inventory_2;
    if (category.contains('Staff')) return Icons.people_alt;
    if (category.contains('Meeting')) return Icons.mic;
    return Icons.description;
  }

  @override
  Widget build(BuildContext context) {
    final docState = ref.watch(docProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Knowledge Base & Document RAG'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Document Index',
            onPressed: () => ref.read(docProvider.notifier).fetchDocuments(),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAlignment.start,
          children: [
            // Upload Area Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppTheme.darkSurface,
                borderRadius: BorderRadius.circular(18),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                crossAxisAlignment: CrossAlignment.start,
                children: [
                  const Text(
                    'Upload Project Knowledge Documents',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Upload Primavera P6 Excel exports, BOQ logs, site memos, or PDFs to index them into the ChromaDB vector engine.',
                    style: TextStyle(fontSize: 13, color: AppTheme.darkTextSecondary),
                  ),
                  const SizedBox(height: 16),

                  // Category Selector Chips
                  const Text(
                    'Select Document Category Tag:',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppTheme.accent),
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: _categories.map((cat) {
                      final isSelected = _selectedCategory == cat;
                      return ChoiceChip(
                        label: Text(cat),
                        selected: isSelected,
                        selectedColor: AppTheme.primary,
                        backgroundColor: AppTheme.darkCard,
                        labelStyle: TextStyle(
                          color: isSelected ? Colors.white : AppTheme.darkTextPrimary,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                          fontSize: 12.5,
                        ),
                        onSelected: (val) {
                          if (val) setState(() => _selectedCategory = cat);
                        },
                      );
                    }).toList(),
                  ),

                  const SizedBox(height: 18),

                  // Dropzone / File Picker Button
                  InkWell(
                    onTap: docState.isUploading ? null : _pickAndUploadFile,
                    borderRadius: BorderRadius.circular(14),
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 16),
                      decoration: BoxDecoration(
                        color: AppTheme.darkBg.withOpacity(0.5),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: AppTheme.primary.withOpacity(0.6),
                          width: 1.5,
                          style: BorderStyle.solid,
                        ),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          if (docState.isUploading) ...[
                            const CircularProgressIndicator(color: AppTheme.accent),
                            const SizedBox(height: 12),
                            const Text(
                              'Indexing chunks into ChromaDB...',
                              style: TextStyle(fontSize: 13, color: AppTheme.accent, fontWeight: FontWeight.w600),
                            ),
                          ] else ...[
                            const Icon(Icons.cloud_upload_outlined, size: 40, color: AppTheme.accent),
                            const SizedBox(height: 10),
                            const Text(
                              'Click or Drop File to Upload & Index',
                              style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                            ),
                            const SizedBox(height: 4),
                            const Text(
                              'Supports: PDF, XLSX, XLS, CSV, TXT',
                              style: TextStyle(fontSize: 12, color: AppTheme.darkTextSecondary),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),

                  if (docState.errorMessage != null) ...[
                    const SizedBox(height: 10),
                    Text(
                      docState.errorMessage!,
                      style: const TextStyle(color: AppTheme.danger, fontSize: 12),
                    ),
                  ],
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Indexed Documents List
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Indexed Project Documents',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                ),
                Text(
                  '${docState.documents.length} files in vector store',
                  style: const TextStyle(fontSize: 12, color: AppTheme.darkTextSecondary),
                ),
              ],
            ),
            const SizedBox(height: 12),

            if (docState.documents.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: AppTheme.darkSurface,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Column(
                  children: const [
                    Icon(Icons.folder_open, size: 40, color: AppTheme.darkTextSecondary),
                    SizedBox(height: 8),
                    Text(
                      'No uploaded documents yet. Upload a schedule or BOQ file above to begin vector search.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 13),
                    ),
                  ],
                ),
              )
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: docState.documents.length,
                separatorBuilder: (_, __) => const SizedBox(height: 10),
                itemBuilder: (context, index) {
                  final doc = docState.documents[index];
                  final dateStr = DateFormat('yyyy-MM-dd hh:mm a').format(doc.uploadedAt);

                  return Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppTheme.darkSurface,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: AppTheme.primary.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Icon(_getCategoryIcon(doc.category), color: AppTheme.accent, size: 22),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAlignment.start,
                            children: [
                              Text(
                                doc.filename,
                                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.darkTextPrimary),
                                overflow: TextOverflow.ellipsis,
                              ),
                              const SizedBox(height: 4),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: const Color(0xFF334155),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      doc.category,
                                      style: const TextStyle(fontSize: 10.5, color: AppTheme.accent),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    '${doc.formattedSize} • ${doc.chunksIndexed} chunks • $dateStr',
                                    style: const TextStyle(fontSize: 11, color: AppTheme.darkTextSecondary),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.verified, color: AppTheme.success, size: 18),
                      ],
                    ),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}
