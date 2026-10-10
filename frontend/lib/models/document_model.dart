class DocumentModel {
  final String documentId;
  final String filename;
  final String category;
  final int fileSizeBytes;
  final int chunksIndexed;
  final DateTime uploadedAt;

  DocumentModel({
    required this.documentId,
    required this.filename,
    required this.category,
    required this.fileSizeBytes,
    required this.chunksIndexed,
    required this.uploadedAt,
  });

  factory DocumentModel.fromJson(Map<String, dynamic> json) {
    return DocumentModel(
      documentId: json['document_id'] ?? '',
      filename: json['filename'] ?? '',
      category: json['category'] ?? 'General',
      fileSizeBytes: json['file_size_bytes'] ?? 0,
      chunksIndexed: json['chunks_indexed'] ?? 0,
      uploadedAt: json['uploaded_at'] != null
          ? DateTime.tryParse(json['uploaded_at']) ?? DateTime.now()
          : DateTime.now(),
    );
  }

  String get formattedSize {
    if (fileSizeBytes < 1024) return '$fileSizeBytes B';
    if (fileSizeBytes < 1024 * 1024) return '${(fileSizeBytes / 1024).toStringAsFixed(1)} KB';
    return '${(fileSizeBytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }
}
