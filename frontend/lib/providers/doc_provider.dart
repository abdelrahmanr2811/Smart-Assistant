import 'dart:typed_data';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/network/api_client.dart';
import '../models/document_model.dart';

class DocState {
  final List<DocumentModel> documents;
  final bool isLoading;
  final bool isUploading;
  final String? uploadSuccessMessage;
  final String? errorMessage;

  DocState({
    this.documents = const [],
    this.isLoading = false,
    this.isUploading = false,
    this.uploadSuccessMessage,
    this.errorMessage,
  });

  DocState copyWith({
    List<DocumentModel>? documents,
    bool? isLoading,
    bool? isUploading,
    String? uploadSuccessMessage,
    String? errorMessage,
  }) {
    return DocState(
      documents: documents ?? this.documents,
      isLoading: isLoading ?? this.isLoading,
      isUploading: isUploading ?? this.isUploading,
      uploadSuccessMessage: uploadSuccessMessage,
      errorMessage: errorMessage,
    );
  }
}

class DocNotifier extends StateNotifier<DocState> {
  final ApiClient _apiClient;

  DocNotifier(this._apiClient) : super(DocState()) {
    fetchDocuments();
  }

  Future<void> fetchDocuments() async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    try {
      final res = await _apiClient.getDocumentsList();
      if (res.statusCode == 200 && res.data is List) {
        final list = (res.data as List).map((d) => DocumentModel.fromJson(d)).toList();
        state = state.copyWith(documents: list, isLoading: false);
      }
    } catch (e) {
      state = state.copyWith(isLoading: false, errorMessage: 'Failed to fetch docs: $e');
    }
  }

  Future<bool> uploadFile({
    required String filePath,
    required String fileName,
    required String category,
    Uint8List? fileBytes,
  }) async {
    state = state.copyWith(isUploading: true, uploadSuccessMessage: null, errorMessage: null);
    try {
      final res = await _apiClient.uploadDocument(
        filePath: filePath,
        fileName: fileName,
        category: category,
        fileBytes: fileBytes,
      );

      if (res.statusCode == 200) {
        state = state.copyWith(
          isUploading: false,
          uploadSuccessMessage: 'File "$fileName" uploaded & indexed under "$category" successfully!',
        );
        fetchDocuments();
        return true;
      } else {
        throw Exception('Upload failed with code ${res.statusCode}');
      }
    } catch (e) {
      state = state.copyWith(
        isUploading: false,
        errorMessage: 'Upload failed: $e',
      );
      return false;
    }
  }
}

final docProvider = StateNotifierProvider<DocNotifier, DocState>((ref) {
  return DocNotifier(ApiClient());
});
